from store.decoraters import allowed_users, unauthenticated_user
from django.http import response
from django.shortcuts import redirect, render
from .models import *
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import CreateUserForm
import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


from .decoraters import unauthenticated_user,admin_only


# @unauthenticated_user

def registerPage(request):
    form=CreateUserForm()
    if request.method == 'POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')
            group=Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
            )
            messages.success(request, 'Account is created for '+ username)
            return redirect('loginPage')

    context={'form': form }
    return render(request, 'store/register.html', context)


# @unauthenticated_user
def loginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "User name or pwd is incorrect")
    else:
        messages.error(request, "User name or pwd is incorrect")


    form=AuthenticationForm()
    return render(request, 'store/login.html')


def logout(request):
    logout(request)
    return redirect('login')
# Create your views here.\

@login_required(login_url='loginPage')

def home(request):
    # this code is only to print no of cart items 
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer, complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        return redirect('loginPage')
        
    # end of printing cart items i looking for another method till its fine
    context={'cartItems': cartItems, }
    return render(request, 'store/home.html', context)




@login_required(login_url='loginPage')
def store(request):
    products=Product.objects.all()
    # # this code is only to print no of cart items 
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer, complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items=[]
        order={'get_grand_total':0, 'get_cart_items':0, 'get_cart_total':0}
        cartItems=order['get_cart_items']
    # end of printing cart items i looking for another method till its fine
    context={'products':products,'cartItems': cartItems }
    return render(request, 'store/store.html', context)


@login_required(login_url='loginPage')
def productdetailview(request,slug):
    q=Product.objects.filter(slug=slug)
    # this code is only to print no of cart items 
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer, complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items=[]
        order={'get_grand_total':0, 'get_cart_items':0, 'get_cart_total':0}
        cartItems=order['get_cart_items']
    # end of printing cart items i looking for another method till its fine
    if q.exists():
        q=q.first()
    else:
        return HttpResponse('<h1>404 Page Not Found</h1>')
    context={'product':q,'cartItems': cartItems }
    return render(request, 'store/productdetailview.html', context)


@login_required(login_url='loginPage')
def cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer, complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items=[]
        order={'get_grand_total':0, 'get_cart_items':0, 'get_cart_total':0}
        cartItems=order['get_cart_items']
        
    context={'items':items, 'order':order, 'cartItems': cartItems,'shipping':False}
    return render(request, 'store/cart.html', context)


@login_required(login_url='loginPage')
def checkout(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer, complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items=[]
        order={'get_grand_total':0, 'get_cart_items':0, 'get_cart_total':0}
        cartItems=order['get_cart_items']
    context={'order':order, 'cartItems':cartItems, 'shipping': False}
    return render(request, 'store/checkout.html', context)


@login_required(login_url='loginPage')
def about(request):
    # this code is only to print no of cart items 
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer, complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items=[]
        order={'get_grand_total':0, 'get_cart_items':0, 'get_cart_total':0}
        cartItems=order['get_cart_items']
    # end of printing cart items i looking for another method till its fine
    context={'cartItems': cartItems}
    return render(request, 'store/about.html', context)

@login_required(login_url='loginPage')
def contact(request):
     # this code is only to print no of cart items 
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer, complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items=[]
        order={'get_grand_total':0, 'get_cart_items':0, 'get_cart_total':0}
        cartItems=order['get_cart_items']
    # end of printing cart items i looking for another method till its fine
    if request.method=='POST':
        print("we are using post request")
        name=request.POST['c_fname']
        phone=request.POST['c_phone']
        email=request.POST['c_email']
        msg=request.POST['c_message']
        contact=Contact(name=name,phone=phone,email=email,msg=msg)
        contact.save()
        messages.success(request, 'your message has been sent')
    context={'cartItems': cartItems}
    return render(request, 'store/contact.html', context)

@login_required(login_url='loginPage')
def updateItem(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']
    print('action',action)
    print('actionid',productId)
    customer=request.user.customer
    product=Product.objects.get(id=productId)
    order, created=Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created=OrderItem.objects.get_or_create(order=order,product=product)
    if action=='add':
        orderItem.quantity=(orderItem.quantity+1)
    elif action == 'remove':
        orderItem.quantity=(orderItem.quantity-1)
    orderItem.save()
    if orderItem.quantity<=0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)


@login_required(login_url='loginPage')
def thankYou(request):
    context={ }
    return render(request, 'store/thankyou.html', context)

# def shippingData(request):
#     if request.method=='POST':
#         address=request.POST.get('username')
#         city=request.POST.get('password')
#         zip=request.POST.get('password')

#         x=User.objects.create_user(address=address,city=city,zip_add=zip)
#         x.save()
#         return redirect('/thankyou.html')

def predict(request):
    context={ }
    return render(request,'store/predict.html', context)

def result(request):
    data_frame = pd.read_csv(r"C:\Users\Khan Saddam\PycharmProjects\medicalstore\diabetes.csv")
    x=data_frame.drop("Outcome", axis=1)
    y=data_frame["Outcome"]

    
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2)
    
    model=LogisticRegression()
    model.fit(x_train,y_train)

    val1= float(request.GET['n1'])
    val2= float(request.GET['n2'])
    val3= float(request.GET['n3'])
    val4= float(request.GET['n4'])
    val5= float(request.GET['n5'])
    val6= float(request.GET['n6'])
    val7= float(request.GET['n7'])
    val8= float(request.GET['n8'])
    
    pred=model.predict([[val1, val2, val3, val4, val5, val6, val7, val8]])
    res=""
    if pred==[1]:
        res="Positive"
    else:
        res="Negative"
    
    return render(request,'store/predict.html', { "result" :res})



@login_required(login_url='loginPage')
def report(request):
    context={ }
    return render(request, 'store/report.html', context)

# def contacts(request):
#     if request.method=='Post':
#         print("we are using post request")
#         name=request.POST['c_fame']
#         phone=request.POST['c_phone']
#         email=request.POST['c_email']
#         msg=request.POST['c_message']
#         contact=Contact(name=name,phone=phone,email=email,msg=msg)
#         contact.save()
#     context={ }
#     return render(request, 'store/contact.html', context)
