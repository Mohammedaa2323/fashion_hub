from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView     #TemplateView #FormView,CreateView,ListView,DetailView,UpdateView,DeleteView
from store.forms import RegistrationForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from store.models import Product
from django.contrib import messages
# Create your views here.

# url- localhost:8000/register/
# method : get,post
# form class Registrationform
class SignupView(View):
    

    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"login.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signin") 
        return render(request,"login.html",{"form":form})

# url- localhost:8000/
# method : get,post
# form class Loginform
    
class SigninView(View):


    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_object=authenticate(request,username=u_name,password=pwd)
            if user_object:
                login(request,user_object)
                return redirect("index")
        messages.error(request,"invalid credontion")
        return render(request,"login.html",{"form":form})

class IndexView(View):


    def get(self,request,*args,**kwargs):
        qs=Product.objects.all()
        return render(request,"index.html",{"data":qs})
    
class ProductlistView(View):


    def get(self,request,*args,**kwargs):
        data=Product.objects.all()
        return render(request,".html",{"data":data})


class ProductDetailView(View):

    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Product.objects.get(id=id)
        return render(request,"product_detail.html",{"data":qs})
    

class HomeView(TemplateView):
    template_name="base.html"
    