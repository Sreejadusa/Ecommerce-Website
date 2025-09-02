from django.shortcuts import render
from django.views import View
from .models import Product,Customer,Cart,Orderplaced,ContactMessage
from django.contrib import messages
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ProductView(View):
    def get(self,request):
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        ac = Product.objects.filter(category='AC')
        tv = Product.objects.filter(category='TV')
        menswear = Product.objects.filter(category='MW')
        womenswear = Product.objects.filter(category='WW')
        watches = Product.objects.filter(category='W')
        footwear = Product.objects.filter(category='FW')
        totalitem = 0
        if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'index.html',locals())

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        if name and email and message:
            ContactMessage.objects.create(name=name, email=email, message=message)
            messages.success(request, "Message sent successfully!")
            return redirect('contact')
        totalitem = 0
        if request.user.is_authenticated:
           totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'contact.html')
      
     
class CategoryView(View):
    def get(self, request,val):
        totalitem = 0
        if request.user.is_authenticated:
           totalitem = len(Cart.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        brand = Product.objects.filter(category=val).values('brand').distinct()
        return render(request, 'category.html',locals())



class CategoryBrand(View):
    def get(self, request, val):
        totalitem = 0
        if request.user.is_authenticated:
           totalitem = len(Cart.objects.filter(user=request.user))
        product = Product.objects.filter(brand=val) 
        category = product.first().category 
        brand = Product.objects.filter(category=category).values('brand').distinct() 
        return render(request, 'category.html', locals())

       
class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        item_already_in_cart = False

        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(product=product, user=request.user).exists()

        totalitem = 0
        if request.user.is_authenticated:
            totalitem = Cart.objects.filter(user=request.user).count()

        return render(request, 'productdetail.html', {
            'product': product,
            'item_already_in_cart': item_already_in_cart,
            'totalitem': totalitem
        })

    



class CustomerRegistrationView(View):
    def get(self, request):
        totalitem = 0
        if request.user.is_authenticated:
           totalitem = len(Cart.objects.filter(user=request.user))
        form = CustomerRegistrationForm()
        return render(request, 'registration.html',locals())   
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():   
           form.save()
           messages.success(request,"Congratulations! User Register Successfully")   
           return redirect('login')
        else:
            messages.warning(request,'Invalid Input Data') 
        return render(request,'registration.html',locals())      


@method_decorator(login_required,name='dispatch')    
class CustomerProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem = 0
        if request.user.is_authenticated:
           totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'profile.html',locals())   
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']

            reg = Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Congratulations! Profile Saved Successfully')
        else:
            messages.warning(request,'Invalid Input Data')    
        return render(request, 'profile.html',locals())   

@login_required     
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,'address.html',locals())

@method_decorator(login_required,name='dispatch')    
class UpdateAddress(View):
    def get(self, request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        if request.user.is_authenticated:
           totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'updateAddress.html',locals())   
    def post(self, request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.locality=form.cleaned_data['locality']
            add.city=form.cleaned_data['city']
            add.mobile=form.cleaned_data['mobile']
            add.state=form.cleaned_data['state']
            add.zipcode=form.cleaned_data['zipcode']
            add.save()
            messages.success(request, 'Congratulations! Profile Updated Successfully')
        else:
            messages.warning(request, 'Invalid Input Data')
        return redirect("address")
    

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    
    return redirect('/cart')

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)  
    amount = 0
    for p in cart:
        value =  p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40  
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'addtocart.html', locals())


@login_required 
def search(request):
    query = request.GET.get('search')
    product = Product.objects.filter(title__icontains=query)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
    return render(request, 'search.html', locals())    


@login_required 
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=request.user)
    cart = Cart.objects.filter(user=user)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    amount = 0
    for p in cart:
        value =  p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    return render(request,'checkout.html',locals())



@login_required       
def payment_done(request):
    user = request.user
    custid = request.POST.get('custid') 
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for p in cart:
        Orderplaced(user=user, customer=customer, product=p.product, quantity=p.quantity).save()
        p.delete()
    return redirect('orders')

    
@login_required 
def orders(request):
    op =  Orderplaced.objects.filter(user=request.user)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,'orders.html',locals())

def plus_cart(request):
    if request.method =='GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(product__id=prod_id, user=request.user)
        c.quantity+= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value =  p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(product__id=prod_id, user=request.user)
        
        if c.quantity > 1:        
            c.quantity -= 1
            c.save()
        
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount += value
        totalamount = amount + 40
        
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)



def remove_cart(request):
    if request.method =='GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(product__id=prod_id, user=request.user)
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value =  p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'amount':amount,
            'totalamount':totalamount,
            'cart_empty': not cart.exists() 
        }
        return JsonResponse(data)




