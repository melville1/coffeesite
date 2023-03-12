from django.shortcuts import render, redirect
from django.views import View
from beansapp.models import Order, Addressee,OrderItem,Guest,Product
from .forms import AddresseeForm,GuestShippingForm,Profile_UpdateForm
from django.forms import inlineformset_factory
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate,login,update_session_auth_hash
from django import http


# Create your views here.

class HomeView(View):
    def get (self,request):

        username = request.user.username
        currentuser  = request.user

        html_data ={ 
        'username':username,
        'currentuser' :currentuser
            }

        


        
        return render(
        request= request,
        template_name= "index.html",
        context= html_data
        )


class OrderView(View):
    def get (self,request):
        products = Product.objects.all()
        products = [dict(image=product.image, title=product.name, description=product.description, price=product.price, product_id=product.id) for product in products]                     
                            
        username = request.user.username
        currentuser  = request.user
        # AnonymousUser = isAnonymousUser
        
        
        html_data ={ 
            'products': products,
            'username':username,
            'currentuser' :currentuser
            }


        return render(
        request= request,
        template_name= "product_page.html",
        context= html_data
        )

    def post(self,request):
        products = list(Product.objects.values_list("id"))
        
        grouped = {}
        for product in products:
            try:
                quantity= request.POST[f"quantity.{product[0]}"]
                grouped[product[0]] = int(quantity) if quantity else 0 
            except KeyError:
                continue
        
        

        # data = dict(quantity=request.POST["quantity"], product=Product.objects.get(id=request.POST["product_id"]), user=request.user.id)
        addressee = request.user # we are getting the addresse - a set up for the following line
        order = Order.objects.create(addressee=addressee) # order is created connecting it to the addressee
        # order_items = OrderItem.objects.create(order=order, product=data["product"], quantity=data["quantity"])
        order_items = [OrderItem(order=order, product=Product.objects.get(id=key), quantity=value) for key, value in grouped.items() if value  ] 
        OrderItem.objects.bulk_create(order_items)
        return http.HttpResponseRedirect(f'../confirmation/{order.id}')

class GuestView(View):
   
    def get (self,request):
        products = Product.objects.all()
        products = [dict(image=product.image, title=product.name, description=product.description, price=product.price, product_id=product.id) for product in products]                     
                            
        username = request.user.username
        currentuser  = request.user
        # AnonymousUser = isAnonymousUser
        
        
        html_data ={ 
            'products': products,
            'username':username,
            'currentuser' :currentuser
            }


        return render(
        request= request,
        template_name= "product_page.html",
        context= html_data
        )

    def post(self,request):
        products = list(Product.objects.values_list("id"))
        
        grouped = {}
        for product in products:
            try:
                quantity= request.POST[f"quantity.{product[0]}"]
                grouped[product[0]] = int(quantity) if quantity else 0 
            except KeyError:
                continue

        order = Order.objects.create() 

        order_items = [OrderItem(order=order, product=Product.objects.get(id=key), quantity=value) for key, value in grouped.items() if value  ] 
        OrderItem.objects.create()
        return http.HttpResponseRedirect(f'../guest_shipping/{order.id}')

class EditView(View):

    def get (self,request,id):
        order = Order.objects.get(id=id)
        order_item = OrderItem.objects.filter(order=order)

        products = Product.objects.all()
        products = [
            dict(
                image=product.image,
                title=product.name,
                description=product.description, 
                price=product.price,
                product_id=product.id, 
                quantity=order_item.filter(product=product).values_list("quantity").first()[0]
            ) if order_item.filter(product=product).exists() else   
            dict(
                image=product.image,
                title=product.name,
                description=product.description, 
                price=product.price,
                product_id=product.id, 
                quantity=0,

            ) for product in products]
            
            


        username = request.user.username
        currentuser  = request.user
        # AnonymousUser = isAnonymousUser
        
        
        html_data ={ 
            'products': products,
            'username':username,
            'currentuser' :currentuser
            }


        return render(
        request= request,
        template_name= "product_page.html",
        context= html_data
        )

       
    def post(self,request,id):
        order = Order.objects.get(id=id)
        products = list(Product.objects.values_list("id"))
        
        grouped = {}
        for product in products:
            try:
                quantity = request.POST[f"quantity.{product[0]}"]
                grouped[product[0]] = int(quantity) if quantity else 0 
            except KeyError:
                continue
        order_items = OrderItem.objects.filter(order=order)
        products_not_included = Product.objects.exclude(
            id__in=order_items.values_list("product__id", flat=True)
        )
        
        new_order_items = [
            OrderItem(order=order, product=product, quantity=grouped[product.id]) for product in products_not_included
            if grouped[product.id]
        ]
        OrderItem.objects.bulk_create(new_order_items)
        for oi in order_items:
            oi.quantity = grouped[oi.product.id]
        order_items = OrderItem.objects.bulk_update(order_items, ["quantity"])
        
        return http.HttpResponseRedirect(f'../confirmation/{order.id}')


class ConfirmationView(View):
    def get (self,request,id): # the id is like a book but only contains the title
        order = Order.objects.get(id=id) # we write this again because we need to acceess the book ( in this case order)
        # the order.objects.get will get me the order associated with id
        # this gets the entire object and all the data that it contains
        orderitems = OrderItem.objects.filter(order=order) # the "_set.all()" is a django method thats allows us
        # to get everything from orderitem in this example.
        item_total = Order.get_order_items(order) 
        order_price = Order.get_total(order)
        
        
        return render(
            request=request,
            template_name='confirmation.html',
            context={
                'order':order,
                'items':orderitems,
                'order_total': item_total,
                'order_price': order_price,
                
                
                
            }
        )
    def post(self,request,id):
        order = Order.objects.get(id=id)
        
        if 'delete' in request.POST:
            order.delete()
            return redirect('home')
               

            
class ReceiptView(View):
    def get (self,request,id):
        order = Order.objects.get(id=id) 
        orderitems = order.orderitem_set.all()
        item_total = Order.get_order_items(order)
        order_price = round(Order.get_total(order),2) 
        username = request.user.username
        
        
        html_data={
            'order':order,
                'items':orderitems,
                'order_total': item_total,
                'order_price': order_price,

                'username':username,
                
            
            }
      
        
        return render(
        request= request,
        template_name= "receipt.html",
        context= html_data
        )



class ProductView(View):


    def get (self,request):
        
        
        return render(
        request= request,
        template_name= "menu.html",
        context= {}
        )

class HistoryOrderView(View):
    def get (self,request):
        addressee = request.user
        addressehistory = Order.objects.filter(addressee=addressee)

        html_data ={
            'addressee':addressee,
            'addressehistory': addressehistory,

        }

        return render(
        request= request,
        template_name= "orderhistory.html",
        context= html_data
        )
    
class RegistrationView(View):
    def get (self,request,id=None):
        
        if id:     # this line of code is not necessary from 233-238
            order = Order.objects.get(id=id)
            
        else:
            order= None
                
        registrationform = AddresseeForm()

        html_data ={ 
            'registrationform': registrationform,
            }
      
        
        return render(
        request= request,
        template_name= "registration.html",
        context= html_data
        )
    
    def post(self,request,id=None):
        form = AddresseeForm(request.POST)
        
        # if registrationform.is_valid():
        if True:
            user = Addressee.objects.create_user(
                username=request.POST["username"],
                email=request.POST["email"],
                password=request.POST["password"],
                first_name=request.POST["first_name"],
                last_name=request.POST["last_name"],
                address=request.POST["address"],
                city=request.POST["city"],
                state=request.POST["state"],
                zipcode=request.POST["zipcode"],
            )
            user.save() # saves it to the database
    
            login(request,user)
            # login(request, new_user)
            # return redirect(to='order' )
        if id:
            order= Order.objects.get(id=id) # when guest registers it hits this line because the order is already created
           
        else:
            order= None
        if not order :       
            
            return redirect(to='order' )
        
        else: 
            order.addressee = user #when guest registers assign to order
            order.guest = None
            order.save()
            return redirect('confirmation', order.id )
        
 

    
class GuestShippingView(View):
    def get(self,request,id):
        order = Order.objects.get(id=id)
        
        currentuser  = request.user

        form = GuestShippingForm(instance=order)
        
       
        html_data ={ 
            'form':form,
            
            'currentuser' :currentuser
            }


        return render(
        request= request,
        template_name= "guest_shipping.html",
        context= html_data
        )

    def post(self,request,id):
        order = Order.objects.get(id=id)
        forminfo = {}
        
      
                        
        
        if not 'create_account' in request.POST:
            guest = Guest.objects.create() # object id is created only
            form = GuestShippingForm(request.POST,instance=guest)
            form.save() 
            order.guest = guest #this is the magic line, this line associates the order with the guest
                # the way it is done is that line 292 creates the guest object id. order.guest = guest goes to the order
                # table and assigns the guest attribute to the id.
            order.save()

        
            return redirect('confirmation',order.id)
        else:
            

            return redirect('guest_registration',order.id)
    
         
class ProfileView(View):
    def get (self,request,):
        addressee = request.user
       

        

        html_data ={ 
        'addressee':addressee,
        }

        
        return render(
        request= request,
        template_name= "profile.html",
        context= html_data
        )


class Profile_UpdateView(View):
    def get (self,request,):  

        addressee = request.user
        profile_updateform = Profile_UpdateForm()

        html_data ={ 
        'addressee':addressee,
        'profile_updateform' : profile_updateform
        }


        return render(
                request= request,
                template_name= "profile_update.html",
                context= html_data
                )

    def post(self,request,):
        user = request.user
        profile_form = Profile_UpdateForm(request.POST,instance=user)
        profile_form.save()


        return redirect('profile')
        
class UserName_UpdateView(View):
    def get (self,request,):
        pass

class AboutView(View):
    
    def get (self,request):
        return render(
            request= request,
            template_name= "about.html",
            context= {}
        )

class BeansView(View):
    
    def get (self,request):
        return render(
            request= request,
            template_name= "starbucks.html",
            context= {}
        )
    
class DunkinView(View):
    
    def get (self,request):
        return render(
            request= request,
            template_name= "dunkin.html",
            context= {}
        )
    
class GregoryView(View):
    
    def get (self,request):
        return render(
            request= request,
            template_name= "gregory.html",
            context= {}
        )