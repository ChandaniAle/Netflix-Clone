from django.contrib import admin
from django.urls import path
from flix import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',views.handleSignUp,name='signup'),
    path('',views.index,name='index'),
    path('home/',views.home,name='home'),
    path('profile/',views.profile,name='profile'),
    path('profile_detail/<int:id>/',views.profile_detail,name='profile_detail'),
    path('profile/create/',views.create_profile,name='create_profile'),
    path('login/',views.handleLogin,name='login'),
    path('logout/',views.handleLogout,name='logout'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('change_password/<str:token>/',views.change_password,name='change_password'),
    path('esewa_request/',views.esewa_request,name='esewa_request'),
    path('video/<str:uuid>/',views.SingleVideoPost,name='video'),
    path('practice/',views.practice,name='practice'),
    path('slider/',views.slider,name='slider'),
    path('search/',views.handleSearch,name='search'),
    path('subscription/',views.subscription_plan,name='subscription'),
    path('payment/',views.handle_payment,name='payment'),
    path('manage/',views.manage_profile,name='manage_profile'),
    path('edit/<int:id>/',views.edit_profile,name='edit_profile'),
    path('transfer/',views.transfer_profile,name='transfer_profile'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

