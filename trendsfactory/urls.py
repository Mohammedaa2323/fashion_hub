"""
URL configuration for trendsfactory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from store import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.SignupView.as_view(),name="signup"),
    path('signin/',views.SigninView.as_view(),name="signin"),
    path('index/',views.IndexView.as_view(),name="index"),
    path('product/<int:pk>/',views.ProductDetailView.as_view(),name="product-detail"),
    path('home',views.HomeView.as_view(),name="home"),
    path('product/<int:pk>/add_to_basket',views.AddToBasketView.as_view(),name="addto-basket"),
    path('basket/items/all/',views.BasketitemListView.as_view(),name="basket-item"),
    path('basket/item/<int:pk>/remove/',views.BasketitemRemoveView.as_view(),name="basketitem-remove"),
    path('basket/item/<int:pk>/qty/change/',views.Cartitemupdatequantityview.as_view(),name="editcart-qty"),
    path('checkout/',views.CheckOutView.as_view(),name="checkout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

