from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView     #TemplateView #FormView,CreateView,ListView,DetailView,UpdateView,DeleteView
from store.forms import RegistrationForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from store.models import Product,BasketItem,Size,Order,OrderItems
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
    
def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("signup")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

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
    

# add to basket
# url- lochalhost:8000/product/(id)/addtobasket/
# method-post
    
class AddToBasketView(View):

    
    def post(self,request,*args,**kwargs):
        size=request.POST.get("size")
        size_obj=Size.objects.get(name=size)
        qty=request.POST.get("qty")
        id=kwargs.get("pk")
        product_obj=Product.objects.get(id=id)
        BasketItem.objects.create(
            size_object=size_obj,
            qty=qty,
            product_object=product_obj,
            basket_object=request.user.cart
        )
        return redirect("index")


# basket items list View
# url-localhost:8000/basket/items/all/
# method:get
    
class BasketitemListView(View):


    def get(self,request,*args,**kwargs):
        qs=request.user.cart.cartitem.filter(is_order_placed=False)
        # qs=BasketItem.objects.filter()
        
        return render(request,"cart_list.html",{"data":qs})
    

class BasketitemRemoveView(View):


    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        basket_item_object=BasketItem.objects.get(id=id)
        basket_item_object.delete()
        return redirect("basket-item")
    

class Cartitemupdatequantityview(View):

    
    def post(self,request,*args,**kwargs):
        action=request.POST.get("counterbutton")
        id=kwargs.get("pk")
        basket_item_object=BasketItem.objects.get(id=id)
        if action=="+":
            basket_item_object.qty+=1
        else:
            basket_item_object.qty-=1
        basket_item_object.save()
        return redirect("basket-item")
    

class CheckOutView(View):


    def get(self,request,*args,**kwargs):
        return render(request,"checkout.html")
    

    def post(self,request,*args,**kwargs):
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        address=request.POST.get("address")

    # creat order_instance
        order_obj=Order.objects.create(


            user_object=request.user,
            delivery_address=address,
            email=email,
            phone=phone,
            total=request.user.cart.basket_total
            
          
        )

             # creat order_item_instance

        try:  #if there any error in this method we can use try
            basket_items=request.user.cart.cart_items
            for bi in basket_items:

                OrderItems.objects.create(
                    order_object=order_obj,
                    basket_item_object=bi

                )
                bi.is_order_placed=True
                bi.save()


        except: # if the method was wrong we also send the solution for the method

            order_obj.delete()

        finally:  # if this method sucsses or wrong this method work allways
           return redirect("index")
    

class OrderSummery(View):


    def get(self,requset,*args,**kwargs):
        qs=OrderItems.objects.all()
        return render(requset,"order_summery.html",{"data":qs})