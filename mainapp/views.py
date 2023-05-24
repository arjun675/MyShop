from django.shortcuts import render,HttpResponseRedirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import auth,messages
from django.contrib.auth.decorators import login_required
from math import prod
import re
def home(request):
    data = Product.objects.all()
    data=data[::-1]
    return render(request,"index.html",{"Data":data})

def shop(request,mc,sc,br):
    if(mc=="all" and sc=='all' and br=='all'):
        data = Product.objects.all()
    elif(mc!='all' and sc=='all' and br=='all'):
        data = Product.objects.filter(maincat=MainCategory.objects.get(name=mc))  
    elif(mc=='all' and sc!='all' and br=='all'):
        data = Product.objects.filter(subcat=SubCategory.objects.get(name=sc))  
    elif(mc=='all' and sc=='all' and br!='all'):
        data = Product.objects.filter(brand=Brand.objects.get(name=br))  
    elif(mc!='all' and sc!='all' and br=='all'):
        data = Product.objects.filter(maincat=MainCategory.objects.get(name=mc),
                                      subcat=SubCategory.objects.get(name=sc))  
    elif(mc=='all' and sc!='all' and br!='all'):
        data = Product.objects.filter(subcat=SubCategory.objects.get(name=sc),
                                      brand=Brand.objects.get(name=br))  
    else:
        data = Product.objects.filter(maincat=MainCategory.objects.get(name=mc),
                                        subcat=SubCategory.objects.get(name=sc),
                                        brand=Brand.objects.get(name=br))                                

          

    maincat = MainCategory.objects.all()
    subcat = SubCategory.objects.all()
    brand = Brand.objects.all()
    return render(request,"shop.html",{"Data":data,"Maincat":maincat,"Subcat":subcat,"Brand":brand,"MC":mc,"SC":sc,"BR":br})    

def product(request,id):
    product = Product.objects.get(id=id)
    if(request.method=="POST"):
        try:
            buyer = Buyer.objects.get(username=request.user)
        except:
            return HttpResponseRedirect("/profile/")
        
        cart = request.session.get('cart',None)
        q = int(request.POST.get('q'))
        if(cart):
            if(str(id) in cart.keys()):
                cart[str(id)]+=int(q)
            else:
                cart.setdefault(str(id),int(q))
        else:
            cart = {str(product.id):q}
        request.session['cart']=cart
        request.session.set_expiry(60*60*24*30)
        return HttpResponseRedirect("/cart/")
    return render(request,"product.html",{"Product":product})

@login_required(login_url='/login/')
def cartPage(request):
    # request.session.flush()
    try:
        buyer = Buyer.objects.get(username=request.user)
    except:
        return HttpResponseRedirect("/profile/")
    cart = request.session.get('cart',None)
    products = []
    total=0
    shipping=0
    final=0
    if(cart):
        for key,value in cart.items():
            
            p = Product.objects.get(id=int(key))
            products.append(p)
            total+= p.finalPrice * value
        if(total<1000):
            shipping = 150
        else:
            shipping = 0
        final = total + shipping
    if(request.method=="POST"):
        id = request.POST.get('id')
        q = int(request.POST.get('q'))
        cart[id] = q
        request.session['cart']=cart
        request.session.set_expiry(60*60*24*30)
        return HttpResponseRedirect("/cart/")
    return render(request,"cart.html",{"Products":products,
                                        "Total":total,
                                        "Shipping":shipping,
                                        "Final":final
                                        })
@login_required(login_url="/login/")
def deleteCart(request,id):
    cart = request.session.get('cart',None)
    if(cart):
        cart.pop(str(id))
        request.session['cart'] = cart
    return HttpResponseRedirect("/cart/")    

@login_required(login_url="/login/")    
def checkout(request):
    try:
        buyer = Buyer.objects.get(username=request.user)
    except:
        return HttpResponseRedirect("/profile/")    
    if(request.method=="POST"):    
        cart = request.session.get("cart",None)    
        if(cart is None):
          return   HttpResponseRedirect("/cart/")
        else:
            check = Checkout()  
            check.buyer = buyer
            check.products=""
            check.total=0
            check.shipping=0
            check.finalAmount=0
            for key,value in cart.items():
                check.product = check.products+key+":"+str(value)+","
                p = Product.objects.get(id=key)
                check.total = p.finalPrice*value
            if(check.total<1000):
                check.shipping=150    
            check.finalAmount=check.total+check.shipping    
            check.save()
            mode=request.POST.get("mode")
            if(mode=="cod"):
                check.save()
                request.session['flushcart']=True
                return HttpResponseRedirect("/confirm/")
            else:
                pass
    else:
        cart = request.session.get('cart',None)
        products = []
        total=0
        shipping=0
        final=0
        if(cart):
            for key,value in cart.items():

                p = Product.objects.get(id=int(key))
                products.append(p)
                total+= p.finalPrice * value
            if(total<1000):
                shipping = 150
            else:
                shipping = 0
            final = total + shipping        

    return render(request,"checkout.html",{"Products":products,
                                        "Total":total,
                                        "Shipping":shipping,
                                        "Final":final,
                                        "User":buyer,
                                        })
                                        
@login_required(login_url='/login/')
def confirmationPage(request):
    return render(request,"confirmation.html")

def login(request):
    if(request.method=="POST"):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        if(user is not None):
            auth.login(request,user)
            if(user.is_superuser):
                return HttpResponseRedirect("/admin/")
            else:
                return HttpResponseRedirect("/shop/all/all/all/")    
        else:
            messages.error(request,"username or password is Incorrect")
    return render(request,'login.html')

def signup(request):
    if(request.method=="POST"):
       actype = request.POST.get('actype')
       if(actype=='seller'):
            s = Seller()
            s.name = request.POST.get("name")
            s.username = request.POST.get("username")
            s.email = request.POST.get("email")
            s.phone = request.POST.get("phone")
            pward = request.POST.get('password')
            
            try:
                user = User.objects.create_user(username=s.username,password=pward)
                user.save()
                s.save()
                return HttpResponseRedirect('/login/')
            except:
                messages.error(request,'username alrady taken!')  
       else:
            b = Buyer()
            b.name = request.POST.get("name")
            b.username = request.POST.get("username")
            b.email = request.POST.get("email")
            b.phone = request.POST.get("phone")
            pward = request.POST.get('password')
            
            try:
                user = User.objects.create_user(username=b.username,password=pward)
                user.save()
                b.save()
                return HttpResponseRedirect('/login/')
            except:
                messages.error(request,'username alrady taken!')         
    return render(request,'signup.html')
@login_required(login_url="/login/")
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url="/login/")
def profile(request):
    user = User.objects.get(username=request.user)
    if(user.is_superuser):
        return HttpResponseRedirect('/admin/')
    try:    
        user = Seller.objects.get(username=request.user)
        return HttpResponseRedirect('/sellerprofile/')
    except:
        user = Buyer.objects.get(username=request.user)
        return HttpResponseRedirect('/buyerprofile/')    
    
@login_required(login_url="/login/")
def sellerprofile(request):
    seller = Seller.objects.get(username=request.user)
    products = Product.objects.filter(seller=seller)
    return render(request,"sellerprofile.html",{"User":seller,"Products":products})

@login_required(login_url="/login/")
def buyerprofile(request):
    buyer = Buyer.objects.get(username=request.user)   
    Wishlist2 = wishlist.objects.filter(buyer=buyer) 
    return render(request,"buyerprofile.html",{"User":buyer,"Wishlist1":Wishlist2})

@login_required(login_url="/login/")
def updateProfile(request):
    user = User.objects.get(username=request.user)
    if(user.is_superuser):
        return HttpResponseRedirect('/admin/')
    try:    
        user = Seller.objects.get(username=request.user)
    except:
        user = Buyer.objects.get(username=request.user)    
    if(request.method=="POST"):
        user.name = request.POST.get("name")
        user.email = request.POST.get("email")
        user.phone = request.POST.get("phone")
        user.addressline1 = request.POST.get("addressline1")
        user.addressline2 = request.POST.get("addressline2")
        user.addressline3 = request.POST.get("addressline3")
        user.pin = request.POST.get("pin")
        user.city = request.POST.get("city")
        user.state = request.POST.get("state")
        if(request.FILES.get('pic')):
            user.pic = request.FILES.get("pic")
        user.save()    
        return HttpResponseRedirect("/profile/")
    return render(request,'updateProfile.html',{"User":user})

@login_required(login_url="/login/")
def updateDetails(request):
    user = Buyer.objects.get(username=request.user)    
    if(request.method=="POST"):
        user.name = request.POST.get("name")
        user.email = request.POST.get("email")
        user.phone = request.POST.get("phone")
        user.addressline1 = request.POST.get("addressline1")
        user.addressline2 = request.POST.get("addressline2")
        user.addressline3 = request.POST.get("addressline3")
        user.pin = request.POST.get("pin")
        user.city = request.POST.get("city")
        user.state = request.POST.get("state")
        user.save()    
        return HttpResponseRedirect("/checkout/")
    return render(request,'buyerprofile.html',{"User":user})    

@login_required(login_url="/login/")
def addProduct(request):
    mainCat = MainCategory.objects.all()
    subCat = SubCategory.objects.all()
    brand = Brand.objects.all()
    seller = Seller.objects.get(username=request.user)
    if(request.method=="POST"):
        p = Product()
        p.seller = seller;
        p.name = request.POST.get("name")
        p.maincat = MainCategory.objects.get(name=request.POST.get("maincategory"))
        p.subcat =  SubCategory.objects.get(name=request.POST.get("subcategory"))
        p.brand = Brand.objects.get(name=request.POST.get("brand"))
        p.basePrice = request.POST.get("basePrice")
        p.discount = request.POST.get("discount")
        p.finalPrice = int(p.basePrice)*int(p.discount)//100
        p.description = request.POST.get('description')
        p.color = request.POST.get("color")
        p.size = request.POST.get("size")
        p.stock = request.POST.get("stock")
        if(request.FILES.get("pic1")):
            p.pic1 = request.FILES.get("pic1")
        if(request.FILES.get("pic2")):
            p.pic2 = request.FILES.get("pic2")
        if(request.FILES.get("pic3")):
            p.pic3 = request.FILES.get("pic3") 
        if(request.FILES.get("pic4")):
            p.pic4 = request.FILES.get("pic4")
        p.save()
        return HttpResponseRedirect('/sellerprofile/')
    return render(request,'addproduct.html',{
                                    "MainCat":mainCat,
                                    "SubCat":subCat,
                                    "Brand":brand
    })

@login_required(login_url="/login/")
def editproduct(request,num):
    mainCat = MainCategory.objects.all()
    subCat = SubCategory.objects.all()
    brand = Brand.objects.all()
    product = Product.objects.get(id=num)
    if(request.method=="POST"):
        product.name = request.POST.get("name")
        product.maincat = MainCategory.objects.get(name=request.POST.get("maincategory"))
        product.subcat =  SubCategory.objects.get(name=request.POST.get("subcategory"))
        product.brand = Brand.objects.get(name=request.POST.get("brand"))
        product.basePrice = request.POST.get("basePrice")
        product.discount = request.POST.get("discount")
        product.finalPrice = int(product.basePrice)*int(product.discount)//100
        product.description = request.POST.get('description')
        product.color = request.POST.get("color")
        product.size = request.POST.get("size")
        product.stock = request.POST.get("stock")
        if(request.FILES.get("pic1")):
            product.pic1 = request.FILES.get("pic1")
        if(request.FILES.get("pic2")):
            product.pic2 = request.FILES.get("pic2")
        if(request.FILES.get("pic3")):
            product.pic3 = request.FILES.get("pic3") 
        if(request.FILES.get("pic4")):
            product.pic4 = request.FILES.get("pic4")
        product.save()
        return HttpResponseRedirect('/sellerprofile/')
    return render(request,'editproduct.html',{
                                    "MainCat":mainCat,
                                    "SubCat":subCat,
                                    "Brand":brand,
                                    "Product":product
    })

@login_required(login_url="/login/")
def deleteProduct(request,num):
    try:
        product = Product.objects.get(id=num)
        seller =  Seller.objects.get(username=request.user)
        if(product.seller==seller):
            product.delete()
    except:
        pass
    return HttpResponseRedirect("/profile/")        

@login_required(login_url="/login/")
def wishlistPage(request,num):
    product = Product.objects.get(id=num)
    try:
        buyer = Buyer.objects.get(username=request.user)
    except:
        return HttpResponseRedirect("/profile/")    
    wishlist1 = wishlist.objects.filter(buyer=buyer)
    flag = False
    for i in wishlist1:
        if(i.product==product):
            flag=True
            break
    if(flag==False):    
        w = wishlist()
        w.buyer=buyer
        w.product=product
        w.save()
    return HttpResponseRedirect("/buyerprofile/")     

@login_required(login_url="/login/")
def deleteWishlist(request,num):
    Wishlist = wishlist.objects.get(id=num)   
    try:                                    
        buyer = Buyer.objects.get(username=request.user)
    except:
        return HttpResponseRedirect("/profile/")    
    if(Wishlist.buyer==buyer):
        Wishlist.delete()
    return HttpResponseRedirect("/buyerprofile/")    



