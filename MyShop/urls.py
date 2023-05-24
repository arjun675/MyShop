
from django.contrib import admin
from django.urls import path
from mainapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.home),
    path("shop/<str:mc>/<str:sc>/<str:br>/",views.shop),
    path("product/<int:id>/",views.product),
    path('login/',views.login),
    path('signup/',views.signup),
    path('logout/',views.logout),
    path('profile/',views.profile),
    path('sellerprofile/',views.sellerprofile),
    path('updateProfile/',views.updateProfile),
    path('addProduct/',views.addProduct),
    path('deleteProduct/<int:num>/',views.deleteProduct),
    path('editproduct/<int:num>/',views.editproduct),
    path("buyerprofile/",views.buyerprofile),
    path("wishlist/<int:num>/",views.wishlistPage),
    path("deleteWishlist/<int:num>/",views.deleteWishlist),
    path("cart/",views.cartPage),
    path("deleteCart/<int:id>/",views.deleteCart),
    path("checkout/",views.checkout),
    path('confirm/',views.confirmationPage),
    path('updateDetails/',views.updateDetails)
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
