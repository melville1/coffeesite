from django.urls import path
from beansapp.views import * 
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from .forms import UsernameForm


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('place_order/' , OrderView.as_view(), name='order' ),
    path('confirmation/<int:id>', ConfirmationView.as_view(), name='confirmation' ),
    path('editorder/<int:id>', EditView.as_view(), name='editorder' ),
    path('receipt/<int:id>', ReceiptView.as_view(), name='receipt' ),
    path('product', ProductView.as_view(), name= 'menu'),
    path('orderhistory/', HistoryOrderView.as_view(), name='orderhistory' ),
    path('registration/', RegistrationView.as_view(), name= 'registration'),
    path('guest_registration/<int:id>', RegistrationView.as_view(), name= 'guest_registration'),
    # path('login', LoginView.as_view(), name= 'login'),
    # path('accounts/', include('django.contrib.auth.urls'),),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'),name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'),name = 'logout'),
    path('guest_view/' , GuestView.as_view(), name='guest' ),
    path('guest_shipping/<int:id>' , GuestShippingView.as_view(), name='guest_shipping' ),
   
    
    path('profile/', ProfileView.as_view(), name='profile' ),
    path('profile_update/', Profile_UpdateView.as_view(), name='profile_update' ),
    path('password_update/', auth_views.PasswordChangeView.as_view(template_name='username_update.html',form_class=UsernameForm,success_url='/profile'),name = 'password_update'),
    path('about/', AboutView.as_view(), name ='about'),
    
    ]
