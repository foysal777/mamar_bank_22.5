
from django.contrib import admin
from django.urls import path,include
from core_app.views import HomeView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view() , name= 'home'),
    path('accounts/', include('account_app.urls')),
    path('transactions/', include('transaction.urls')),
    # path('core_app/', include('core_app.urls')),
]
