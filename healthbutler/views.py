from django.shortcuts import render,get_object_or_404,redirect
import time
from datetime import date
from .forms import SearchForm,UserRegistrationForm,UserEditForm, ProfileEditForm
from .models import Foods,FoodTypes,CheckIn,QuestionAndAnswer,Profile
from django.contrib.auth.decorators import login_required
from cart.forms import CartAddFoodForm
from .utils import Jwt
from django.contrib import messages
from django.conf import settings



# Create your views here

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
        # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
        # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
        # Save the User object
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request,'register_done.html',{'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'register.html',{'user_form': user_form})

def logout(request):
    request.session.clear()
    messages.info(request, 'Log out succeed!')
    return redirect('/healthbutler/Login')

def home(request):
    return render(request, 'base.html')

def food_list(request,fcategory_slug=None):
    fcategory = None
    fcategories = FoodTypes.objects.all()
    foods = Foods.objects.all()
    if fcategory_slug:
        fcategory = get_object_or_404(FoodTypes, slug=fcategory_slug)
        foods = foods.filter(fcategory=fcategory)
    return render(request,'food.html',{'fcategory': fcategory,'fcategories': fcategories,'foods': foods})

def food_detail(request, id,slug):
    food = get_object_or_404(Foods,id=id,slug=slug)
    cart_food_form = CartAddFoodForm()
    return render(request,
                  'detail.html',
                  {'food':food,'cart_food_form':cart_food_form})

@login_required
def dashboard(request):
    return render(request,'dashboard.html',{'section': 'dashboard'})

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        results = Foods.objects.filter(name__contains=query)
    return render(request,'search.html', {'form': form,'query': query,'results': results})

def get_user_info(request):
    user_data = {}
    if request.user.id:
        user_data["user_id"] = request.user.id
    return user_data

def health_qa(request):
    user_data = get_user_info(request)
    qa_data_col1 = []
    qa_data_col2 = []
    qa_data_col3 = []
    qas = QuestionAndAnswer.objects.all()
    length = qas.count()
    if length > 0:
        qa_data_col1 = qas[:length//3]
        qa_data_col2 = qas[length//3:length*2//3]
        qa_data_col3 = qas[length*2//3:length]
    return render(request, 'health_qa.html', dict(qa_data_col1=qa_data_col1, qa_data_col2=qa_data_col2, qa_data_col3=qa_data_col3, **user_data))


def health_qa_detail(request, id):
    user_data = get_user_info(request)
    qa_data = QuestionAndAnswer.objects.get(id=id)
    content_list = qa_data.content.split("\r\n")
    return render(request, 'health_qa_detail.html', dict(qa_data=qa_data, content_list=content_list, **user_data))

def get_check_in_data(user_id):
    check_in_data = []
    today = int(time.mktime(date.today().timetuple()))
    check_in_list = CheckIn.objects.filter(user_id=user_id)
    if len(check_in_list) == 0:
        CheckIn.objects.create(user_id=user_id,name=CheckIn.default_item,check_in_day=today,days=1)
        check_in_data = [dict(name=CheckIn.default_item, days=1, checked=1, color="#00C3B3")]
    else:
        for i, check_in in enumerate(check_in_list):
            color = "#00C3B3" if i == 0 else "#5EB4EF"
            if check_in.check_in_day + check_in.days*24*3600 > today:
                check_in_data.append(dict(name=check_in.name, days=check_in.days, checked=1, color=color, icon=check_in.get_icon()))
            elif check_in.check_in_day + check_in.days*24*3600 == today:
                check_in_data.append(dict(name=check_in.name, days=check_in.days, checked=0, color=color, icon=check_in.get_icon()))
            else:
                check_in_data.append(dict(name=check_in.name, days=0, checked=0, color=color, icon=check_in.get_icon()))
    return check_in_data

@login_required
def health_checkin(request):
    user_data = get_user_info(request)
    check_in_data = []
    if user_data.get("user_id"):
        if request.method == "POST":
            name = request.POST.get("name")
            check_in = CheckIn.objects.get(user_id=user_data.get("user_id"), name=name)
            today = int(time.mktime(date.today().timetuple()))
            if check_in.check_in_day + check_in.days*24*3600 == today:
                check_in.days +=1
            elif check_in.check_in_day + check_in.days*24*3600 < today:
                check_in.check_in_day = today
                check_in.days = 1
            check_in.save()
        check_in_data = get_check_in_data(user_data.get("user_id"))
    else:
        print(1)
    return render(request, 'health_checkin.html', {"check_in_data": check_in_data, **user_data})

def read(request):
    food = Foods.objects.all()
    context = {'food': food}
    return render(request, 'read.html', context)


def add(request):
    if request.method == "POST":
        try:
            food = Foods()
            food.fcategory_id = request.POST['fcategory_id']
            food.name = request.POST['name']
            food.slug = request.POST['slug']
            food.calories = request.POST['calories']
            food.serving = request.POST['serving']
            food.fat = request.POST['fat']
            food.carbs = request.POST['carbs']
            food.fiber = request.POST['fiber']
            food.protein = request.POST['protein']
            food.save()
            return render(request, 'info.html', {"info": "add successfully！"})
        except:
            return render(request, 'info.html', {"info": "add unsuccessfully！"})
    else:
        return render(request, 'add.html')

def  edit(request, id):
    if request.method == "POST":
        try:
            ob = Foods.objects.get(id=id)
            ob.name = request.POST['name']
            ob.calories = request.POST['calories']
            ob.fat = request.POST['fat']
            ob.carbs = request.POST['carbs']
            ob.fiber = request.POST['fiber']
            ob.protein = request.POST['protein']
            ob.save()
            return render(request, 'info.html', {"info": "Edit successfully！"})
        except:
            return render(request, 'info.html', {"info": "Edit unsuccessfully!"})
    else:
        food = Foods.objects.get(id=id)
        context = {'id': food}
        return render(request, 'edit.html', context)


def dele(request, id):
    try:
        food = Foods.objects.get(id=id)
        food.delete()
        return render(request, 'info.html', {"info": "Delete successfully!"})
    except:
        return render(request, 'info.html', {"info": "Delete unsuccessfully!"})

@login_required
def useredit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(
        instance=request.user.profile,
        data=request.POST,
        files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,'useredit.html',{'user_form': user_form,'profile_form': profile_form})



