from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.models import *
from .filters import OrderFilter
from .decorators import *
from .forms import *
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
 
@login_required(login_url='login')
@admin_only
def home(request):

    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    pending_orders = Order.objects.filter(status='Pending').count()
    delivered_orders = Order.objects.filter(status='Delivered').count()

    context = {
        'orders':orders,
        'customers':customers,
        'total_orders':total_orders,
        'pending_orders':pending_orders,
        'delivered_orders':delivered_orders

    }

    return render(request, 'accounts/dashboard.html', context)


def products(request):
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {'products':products})


def customer(request, id):
    customer = Customer.objects.get(id=id)

    orders = customer.order_set.all()
    orders_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
        'customer':customer,
        'orders':orders,
        'orders_count':orders_count,
        'myFilter':myFilter
    }

    return render(request, 'accounts/customers.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def createOrder(request, id):

    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'), extra=5)

    customer = Customer.objects.get(id=id)

    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)

    # form = OrderForm(initial={'customer':customer})

    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
        
    context = {
        'formset' :  formset
    }

    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def updateOrder(request, id):

    order = Order.objects.get(id=id)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context = {
        'form' :  form
    }

    return render(request, 'accounts/update_form.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def deleteOrder(request, id):
    order = Order.objects.get(id=id)
    if request.method == 'POST':
            order.delete()
            return redirect('/')
    
    context = {
        'order':order
    }    

    return render(request, 'accounts/delete_order.html', context)

@unauthenticated_user
def register(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            # grp = Group.objects.get(name='customer')
            # user.groups.add(grp)

            # Customer.objects.create(
            #     user = user,
            #     name = user.username,
            # )

            messages.success(request, 'Account was Created for'+' '+ username)
            return redirect('login')
    
    context ={
        'form':form
    }

    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginUser(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'Username or Password is incorrect')
            
    context ={}

    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    messages.info(request, 'User logged out successfully')
    return redirect('home')

@login_required
@allowed_user(allowed_roles=['customer'])
def userPage(request):

    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    pending_orders = orders.filter(status='Pending').count()
    delivered_orders = orders.filter(status='Delivered').count()

    context = {
        'orders':orders,
        'total_orders':total_orders,
        'pending_orders':pending_orders,
        'delivered_orders':delivered_orders

    }

    return render(request, 'accounts/user.html', context)


@login_required
@allowed_user(allowed_roles=['customer'])
def accountSettings(request):

    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()


    context = {'form':form}

    return render(request, 'accounts/account_settings.html', context)