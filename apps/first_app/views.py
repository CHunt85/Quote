from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request,'first_app/index.html')

def login_fun(request):
    errors = User.objects.login_manager(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['user_firstname']= user.first_name
        request.session['user_lastname']= user.last_name
        request.session['user_email']= user.email        

    return redirect ('/quotes')

def create(request):
    errors = User.objects.basic_validator(request.POST)
    hash_pass = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    user = User.objects.create( first_name= request.POST['first_name'],last_name= request.POST['last_name'],email= request.POST['email'], password= hash_pass )
    user = User.objects.get(email=request.POST['email'])
    request.session['user_firstname']= user.first_name
    request.session['user_lastname']= user.last_name
    request.session['user_email']= user.email
    return redirect('/quotes')

def quotes(request):
    if "user_email" not in request.session:
        return redirect('/')
    else:
        context = {
            'main_u': Quote.objects.filter(like = User.objects.get(email= request.session['user_email'])),
            'users_o': Quote.objects.exclude(like = User.objects.get(email = request.session['user_email'])),
            'message': Quote.objects.all(),
            'auth': Author.objects.all()
        }
    return render (request, 'first_app/quotes.html', context)

def add_fun(request):
    errors = Quote.objects.quote_manager(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/quotes')
    y = User.objects.get(email= request.session['user_email'])
    z = Author.objects.create(name= request.POST['content1'])
    x = Quote.objects.create( quote= y, post= request.POST['content2'])
    x.like.add(y)
    return redirect('/quotes')

def like(request):
    if request.method == "POST":
        liked = Quotes.objects.like(request.POST)
        return redirect('/quotes')

def edit(request):
    if "user_email" not in request.session:
        return redirect('/')
    else:
        return render(request,'first_app/edit.html')

def edit_fun(request):
    errors = User.objects.edit_man(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/edit')
    x = User.objects.first()
    x.name = 'first_name'
    y = User.objects.second()
    y.name = "last_name"
    z = User.objects.third()
    z.email = 'email'
    x.save()
    y.save()
    z.save()
    return redirect('/quotes')

def info(request, id):
    if "user_email" not in request.session:
        return redirect('/')
    else:
        context = {
            'main_q': Quote.objects.get(id = id),
            'users_a': User.objects.get(liked= Quote.objects.get(id = id))
        }
        return render(request,'first_app/info.html')

def destroy(request):
    y= Author.objects.get(id=request.POST['product'])
    x= Quote.objects.get(id=request.POST['product'])
    x.delete()
    y.delete()
    return redirect('/quotes')

def logout(request):
    request.session.clear()
    return redirect ('/')