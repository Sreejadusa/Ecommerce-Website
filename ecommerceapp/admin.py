from django.contrib import admin
from .models import Product,Customer,Cart,Orderplaced,ContactMessage

@admin.register(ContactMessage)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ['id','name','email','message','submitted_at'] 

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','title','selling_price', 'discounted_price','description','brand','category','product_image'] 

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','locality', 'city','state','zipcode'] 

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity'] 


@admin.register(Orderplaced)
class OrderPlacedtModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','product','quantity','ordered_date','status'] 


