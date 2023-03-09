from django.forms import ModelForm
from beansapp.models import  Order,OrderItem,Addressee,Guest
from django.contrib.auth.forms import PasswordChangeForm





class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['addressee']

class AddresseeForm(ModelForm):
    class Meta:
        model= Addressee
        fields=['first_name','last_name','address','city','state','zipcode','phone_number','username','password','email'] 

class Profile_UpdateForm(ModelForm):
    class Meta:
        model= Addressee
        fields=['first_name','last_name','address','city','state','zipcode','phone_number'] 


class UsernameForm(PasswordChangeForm):
    pass
    
    

class GuestShippingForm(ModelForm):
    class Meta:
        model = Guest
        fields = "__all__"


