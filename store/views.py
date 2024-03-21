from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView     #TemplateView #FormView,CreateView,ListView,DetailView,UpdateView,DeleteView
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils.decorators import method_decorator  #
from django.views.decorators.cache import never_cache
from store.forms import RegistrationForm,LoginForm
from store.models import Product,BasketItem,Size,Order,OrderItems,Category,Tags
from store.decoretors import signin_required,owner_permission_required
from django.views.decorators.csrf import csrf_exempt
import razorpay




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


@method_decorator([signin_required,never_cache],name="dispatch")
class IndexView(View):


    def get(self,request,*args,**kwargs):
        qs=Product.objects.all()
        category=Category.objects.all()
        tags=Tags.objects.all()
        selected_category=request.GET.get("categorys")
        if selected_category:
            qs=qs.filter(category_object__name=selected_category)
        return render(request,"index.html",{"data":qs,"categorys":category,"tags":tags})
    
    
    def post(self,request,*args,**kwargs):


        tag_name=request.POST.get("tag")
        qs=Product.objects.filter(tag_objects__name=tag_name)
        return render(request,"index.html",{"data":qs})

@method_decorator([signin_required,never_cache],name="dispatch")
class ProductlistView(View):


    def get(self,request,*args,**kwargs):
        data=Product.objects.all()
        return render(request,".html",{"data":data})


@method_decorator([signin_required,never_cache],name="dispatch")
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


@method_decorator([signin_required,never_cache],name="dispatch")
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

@method_decorator([signin_required,never_cache],name="dispatch")
class BasketitemListView(View):


    def get(self,request,*args,**kwargs):
        qs=request.user.cart.cartitem.filter(is_order_placed=False)
        # qs=BasketItem.objects.filter()
        
        return render(request,"cart_list.html",{"data":qs})
    

@method_decorator([signin_required,owner_permission_required],name="dispatch")

class BasketitemRemoveView(View):


    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        basket_item_object=BasketItem.objects.get(id=id)
        basket_item_object.delete()
        return redirect("basket-item")
    

@method_decorator([signin_required,owner_permission_required],name="dispatch")
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
    


@method_decorator([signin_required,never_cache],name="dispatch")
class CheckOutView(View):


    def get(self,request,*args,**kwargs):
        return render(request,"checkout.html")
    

    def post(self,request,*args,**kwargs):
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        address=request.POST.get("address")
        payment_method=request.POST.get("payment")

    # creat order_instance
        order_obj=Order.objects.create(


            user_object=request.user,
            delivery_address=address,
            email=email,
            phone=phone,
            total=request.user.cart.basket_total,
            payment=payment_method
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
           
           if payment_method=="online" and order_obj:
                            
                client = razorpay.Client(auth=(KEY_ID,KEY_SECRET))

                data = { "amount": order_obj.get_order_total*100, "currency": "INR", "receipt": "order_rcptid_11" }
                payment = client.order.create(data=data)

                order_obj.order_id=payment.get("id")
                order_obj.save()

                print("payment initiate",payment)
                context={
                    "key":KEY_ID,
                    "order_id":payment.get("id"),
                    "amount":payment.get("amount")
                }
                return render(request,"payment.html",{"context":context})
           return redirect("index")
        

@method_decorator([signin_required,never_cache],name="dispatch")
class SignoutView(View):


    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
    


class OrderSummery(View):


    def get(self,requset,*args,**kwargs):
        # is_order=requset.user.purchase.all()
        is_order=Order.objects.filter(user_object=requset.user).exclude(status="cancelled")
        return render(requset,"order_summery.html",{"data":is_order})
    

    
class OrderItemsRemove(View):


    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        OrderItems.objects.get(id=id).delete()
        return redirect('order-summery')
    
@method_decorator(csrf_exempt,name="dispatch")
class PaymentVarificationView(View):

    def post(self,request,*args,**kwargs):
        client=razorpay.Client(auth=(KEY_ID,KEY_SECRET))
        data=request.POST

        try:
            client.utility.verify_payment_signature(data)
            order_obj=Order.objects.get(order_id=data.get("razorpay_order_id"))
            order_obj.is_paid=True
            order_obj.save()
            print("************ Transaction complete********")
        except:
            print("!!!!!!!!!!!!!transaction falid!!!!!!!!!")

        return redirect("order-summery")