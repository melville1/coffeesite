from django.shortcuts import render, redirect
from django.views import View
from beansapp.models import Order, Addressee,OrderItem,Guest
from .forms import AddresseeForm,GuestShippingForm,Profile_UpdateForm
from django.forms import inlineformset_factory
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate,login,update_session_auth_hash


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
                                    # The orders will be associated with the Order table
                                    # second arguments specifies which table it will use to make forms
                                    # we are then able to make one form from these 2 tables.
        OrderItemFormset = inlineformset_factory(Order,OrderItem, fields=['product','quantity'])
        #inlineformfactory allow you to create multiple forms at once. makes it more efficient.
        # # the form will only only contain attributes that are contain within orderitem table 
        formset = OrderItemFormset() #because line 28  is returning a function we have paranthesis.
        username = request.user.username
        currentuser  = request.user
        # AnonymousUser = isAnonymousUser
        
        
        html_data ={ 
            'formset':formset,
            'username':username,
            'currentuser' :currentuser
            }


        return render(
        request= request,
        template_name= "order.html",
        context= html_data
        )

    def post(self,request):
        OrderItemFormset = inlineformset_factory(Order,OrderItem, fields=['product','quantity'])
        addressee = request.user # we are getting the addresse - a set up for the following line
        order = Order.objects.create(addressee=addressee) # order is created connecting it to the addressee
        formset = OrderItemFormset(request.POST, instance=order)
        # we are calling the OrderItemFormset and filling it with the post data and then associating with the 
        # order from line 47 the "instance" in this case means associating with the order
        # what is happening here is that line 45 calls the form because the post needs it, then 
        # we get the adresse id this is the set up for the follwing line (47)because we will then 
        # create an order and associate it with the addressee and his/her info
        #line 48 then passes the data that was created from the addresse which he created in the post and associates 
        # to the order from line 47.
        if formset.is_valid():
            formset.save() # this adds the data to the database that come from the formset
        return redirect('confirmation', order.id ) # this redirects us to confirmation 
        # the second argument "create.id" grabs the id from the order it does this because an object was created
        # from line 47, therefore we not only access to the id but any other attribute that object may contain
        # keep in mind this order.id now contains data

class GuestView(View):
   
    def get (self,request):
                                
        OrderItemFormset = inlineformset_factory(Order,OrderItem, fields=['product','quantity'])
        
        formset = OrderItemFormset() 
        username = request.user.username
        currentuser  = request.user
        # AnonymousUser = isAnonymousUser
        print(currentuser)
        
        html_data ={ 
            'formset':formset,
            'username':username,
            'currentuser' :currentuser
            }


        return render(
        request= request,
        template_name= "order.html",
        context= html_data
        )

    def post(self,request):
        OrderItemFormset = inlineformset_factory(Order,OrderItem, fields=['product','quantity'])
        order = Order.objects.create() 
        formset = OrderItemFormset(request.POST,instance=order)
       
        if formset.is_valid():
            formset.save() # 
        return redirect('guest_shipping', order.id) 

class EditView(View):

    def get (self,request,id):
        order = Order.objects.get(id=id)
        OrderFormset = inlineformset_factory(Order,OrderItem, fields=['product','quantity'],)
        formset = OrderFormset(instance=order)
    # the order id is from the previous view here we are accessing and displaying that order 
    # which is why you see it prefilled. 
        html_data ={ 
            'formset':formset
            }


        return render(
        request= request,
        template_name= "order.html",
        context= html_data
        )

       
    def post(self,request,id):
        order= Order.objects.get(id=id) # this retrieves the order but has the old data 
        OrderFormset = inlineformset_factory(Order,OrderItem, fields=['product','quantity'],) # making the formset
        formset = OrderFormset(request.POST, instance=order) 
        #line 87 whatever new data was put in the post whether it remains the same or not gets resent to the form
        # associated with that orderid 
        if formset.is_valid():
            formset.save() # saves it to the database
        return redirect('confirmation', order.id ) # redirects us to the confirmation with the orderid associated with


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
