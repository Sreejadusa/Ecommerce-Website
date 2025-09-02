from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordChangeForm, PasswordResetForm, MySetPasswordForm

urlpatterns = [
    path("", views.ProductView.as_view(),name='home'),
    path('contact/',views.contact, name='contact'),
    path("category/<slug:val>", views.CategoryView.as_view(), name="category"),
    path("category-brand/<val>", views.CategoryBrand.as_view(), name="category-brand"),
    path("product-detail/<int:pk>", views.ProductDetailView.as_view(), name="product-detail"),
    path("profile/", views.CustomerProfileView.as_view(), name="profile"),
    path("address/", views.address, name="address"),
    path("updateAddress/<int:pk>", views.UpdateAddress.as_view(), name="updateAddress"),


    path("add-to-cart/",views.add_to_cart,name="add-to-cart"),
    path("cart/",views.show_cart,name="showcart"),
    path('checkout/',views.checkout,name='checkout'),
    path('paymentdone/',views.payment_done,name='paymentdone'),
    path('orders/',views.orders,name='orders'),
    path('search/',views.search,name="search"),

    path("pluscart/",views.plus_cart),
    path("minuscart/",views.minus_cart),
    path('removecart/', views.remove_cart),
    
    
    path("registration/", views.CustomerRegistrationView.as_view(), name="registration"),
    path("login/", auth_view.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name="login"), 
    path("passwordchange/", auth_view.PasswordChangeView.as_view( template_name='changepassword.html',form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name="passwordchange"),
    path("passwordchangedone/", auth_view.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'), name="passwordchangedone"),
    path("logout/", auth_view.LogoutView.as_view(next_page='login'), name='logout'),
    

    path("password-reset/", auth_view.PasswordResetView.as_view(template_name='password_reset.html',form_class=PasswordResetForm), name="password-reset"),
    path("password-reset/done/", auth_view.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_view.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',form_class=MySetPasswordForm), name="password_reset_confirm"),
    path("password-reset-complete/", auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name="password_reset_complete"),
]
