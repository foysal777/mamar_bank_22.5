
from .import views 
from django.urls import path
from .views import UserBankAccountUpdateView


urlpatterns = [
 
  path('register/' , views.RegistrationView.as_view() , name = 'register'),
  path('log_in/' , views.login_View.as_view() , name = 'login'),
  path('log_out/' , views.log_outView.as_view() , name = 'logout'),
  path('profile/', UserBankAccountUpdateView.as_view(), name='profile' )
]
