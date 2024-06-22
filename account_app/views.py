from django.shortcuts import render,redirect
from django.views.generic import FormView,View
from .forms import RegistrationForm ,UserUpdateForm
from django.contrib.auth import login,logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView
# Create your views here.
class RegistrationView(FormView):
    template_name ='register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('register')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request , user)
        print(user)
        return super().form_valid(form)
    
    
class login_View(LoginView):
    template_name = 'log_in.html'
    def get_success_url(self):
        return reverse_lazy('home')
    

class log_outView(LogoutView):
   
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')    
    
class UserBankAccountUpdateView(View):
    template_name = 'profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user's profile page
        return render(request, self.template_name, {'form': form})
    