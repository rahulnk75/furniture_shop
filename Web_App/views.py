from django.shortcuts import render,redirect
from Furniture_app.models import Product_Db,Category_Db
from Web_App.models import Contact_Db,SignUp_Db,Cart_Db,Order_Db
from django.contrib import messages
import razorpay


# Create your views here.
def Home_Page(request):
    cart_count=Cart_Db.objects.filter(User_name=request.session['Name'])
    count=cart_count.count()
    cat_d=Category_Db.objects.all()
    return render(request,'home.html',{'cat_d':cat_d,'count':count})

def product_page(request):
    cat_d=Category_Db.objects.all()
    products=Product_Db.objects.all()
    cart_count=Cart_Db.objects.filter(User_name=request.session['Name'])
    count=cart_count.count()
    return render(request,'product_page.html',{'products':products,'count':count,'cat_d':cat_d})

def about_page(request):
    cat_d=Category_Db.objects.all()
    cart_count=Cart_Db.objects.filter(User_name=request.session['Name'])
    count=cart_count.count()
    return render(request,'about_page.html',{'count':count,'cat_d':cat_d})

def contact_page(request):
    cat_d=Category_Db.objects.all()
    cart_count=Cart_Db.objects.filter(User_name=request.session['Name'])
    count=cart_count.count()
    return render(request,'contact_page.html',{'count':count,'cat_d':cat_d})

def services_page(request):
    cat_d=Category_Db.objects.all()
    cart_count=Cart_Db.objects.filter(User_name=request.session['Name'])
    count=cart_count.count()
    return render(request,'services_page.html',{'count':count,'cat_d':cat_d})

def blog_page(request):
    cat_d=Category_Db.objects.all()
    cart_count=Cart_Db.objects.filter(User_name=request.session['Name'])
    count=cart_count.count()
    return render(request,'blog_page.html',{'count':count,'cat_d':cat_d})

def save_contact(request):
    if request.method == 'POST':
        fname=request.POST.get('fname_')
        lname=request.POST.get('lname_')
        email=request.POST.get('email_')
        message=request.POST.get('message_')
        obj=Contact_Db(First_name=fname,Last_name=lname,Email=email,Message=message)
        obj.save()
        return redirect(contact_page)
    
def product_filtered(request,cat_name):
    cat_d=Category_Db.objects.all()
    data=Product_Db.objects.filter(Product_Category=cat_name)
    return render(request,'product_filtered.html',{'data':data,'cat_d':cat_d})
    
def single_product(request,sin_id):
    cat_d=Category_Db.objects.all()
    sing=Product_Db.objects.get(id=sin_id)
    cart_count=Cart_Db.objects.filter(User_name=request.session['Name'])
    count=cart_count.count()
    return render(request,'single_product.html',{'sing':sing,'count':count,'cat_d':cat_d})

def Sign_up(request):
    return render(request,'sign_up.html')

def Save_Sign_up(request):
    if request.method=='POST':
        _name=request.POST.get('name_')
        _mobile_number=request.POST.get('mobile_number_')
        _email=request.POST.get('email_')
        _Password=request.POST.get('Password_')
        _re_pass=request.POST.get('re_pass_')
        obj=SignUp_Db(Name=_name,Mobile_number=_mobile_number,Email=_email,Password=_Password,Repeat_Password=_re_pass)
        
        if SignUp_Db.objects.filter(Name=_name).exists():
            messages.warning(request,"User already exist..!!")
            return redirect(Sign_up)
        
        elif SignUp_Db.objects.filter(Email=_email).exists():
            messages.warning(request,"Email already exist..!!")
            return redirect(Sign_up)
        
        obj.save()
        return redirect(Sign_up)

def Sign_in(request):
    return render(request,'Sign_in.html')

def User_Sign_in(request):
    if request.method=='POST':
        _username=request.POST.get('name_')
        _password=request.POST.get('password_')
        if SignUp_Db.objects.filter(Name=_username,Password=_password).exists():
            request.session['Name']=_username
            request.session['Password']=_password
            messages.success(request,"Login successfully...!!!")
            return redirect(Home_Page)
        else:
            messages.info(request,"password incorect...!!!")
            return redirect(Sign_in)
    else:
        messages.error(request,"Invalid Username...!!!")
        return redirect(Sign_in)

def User_Sign_out(request):
    del request.session['Name']
    del request.session['Password']
    messages.info(request,"Logout successfully...!!!")
    return redirect(Sign_in)

def Save_Cart(request):
    if request.method=='POST':
        _user_name=request.POST.get('user_name_')
        _product_name=request.POST.get('product_name_')
        _total=request.POST.get('total_')
        _price=request.POST.get('price_')
        _quantity=request.POST.get('quantity_')
        try:
            x = Product_Db.objects.get(Product_Name=_product_name)
            img=x.Product_Image1
        except Product_Db.DoesNotExist:
            img=None
        obj=Cart_Db(User_name=_user_name,Product_name=_product_name,Quantity=_quantity,Price=_price,Total_Price=_total,product_image=img)
        obj.save()
        messages.success(request,"item added to cart")
        return redirect(Cart_Page)
    
def Cart_Page(request):
    cat_d=Category_Db.objects.all()
    obj=Cart_Db.objects.filter(User_name=request.session['Name'])
    Sub_total=0
    Shipping_amount=0
    total_amount=0
    for i in obj:
        Sub_total = Sub_total+i.Total_Price
        if Sub_total>50000:
            Shipping_amount = 100
        else:
            Shipping_amount = 250
        total_amount = Shipping_amount + Sub_total 
    

    return render(request,'cart.html',{'obj':obj,'Sub_total':Sub_total,'total_amount':total_amount,'Shipping_amount':Shipping_amount,'cat_d':cat_d})

def Cart_delete(request,del_id):
    remove=Cart_Db.objects.filter(id=del_id)
    remove.delete()
    messages.success(request,'item removed from cart..!!')
    return redirect(Cart_Page)

def Proceed_CheckOut(request):
    cat_d=Category_Db.objects.all()
    obj=Cart_Db.objects.filter(User_name=request.session['Name'])
    Sub_total=0
    Shipping_amount=0
    total_amount=0
    for i in obj:
        Sub_total = Sub_total+i.Total_Price
        if Sub_total>50000:
            Shipping_amount = 100
        else:
            Shipping_amount = 250
        total_amount = Shipping_amount + Sub_total 
    return render(request,'proceed_checkout.html',{'obj':obj,'Sub_total':Sub_total,'total_amount':total_amount,'Shipping_amount':Shipping_amount,'cat_d':cat_d})
   
        
def Order_Save(request):
    if request.method=='POST':
        name=request.POST.get('name_')
        email=request.POST.get('email_')
        phone=request.POST.get('phone_')
        place=request.POST.get('place_')
        total=request.POST.get('total_')
        address=request.POST.get('address_')
        message=request.POST.get('message_')
        obj=Order_Db(Name=name,Email=email,Phone=phone,Place=place,total=total,Address=address,Message=message)
        obj.save()
        return redirect(Payment_Page)
    
def Payment_Page(request):
    customer=Order_Db.objects.order_by('-id').first()
    payy=customer.total
    amount=int(payy*100)
    payy_str=str(amount)
    if request.method=="POST":
        order_currency= 'INR'
        client=razorpay.Client(auth=('rzp_test_sXSjc7ZbwI7M3J','JfZlKEyC2d0YJZDzcHX4eMjP'))
        payment = client.order.create({'amount':amount,'order_currency':order_currency})

    return render(request,'payment_page.html',{'customer':customer,'payy_str':payy_str})





        
