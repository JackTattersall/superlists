from django.shortcuts import redirect, render
from .models import Item, List
from .forms import ItemForm, ExistingListItemForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/login/')
def home_page(request):
    return render(request, 'home.html', {"form": ItemForm()})


@login_required(login_url='/login/')
def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, "form": form})


@login_required(login_url='/login')
def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form": form})


def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return redirect('/login')
        else:
            return render(request, 'login.html', {"form": form})
    else:
        return render(request, 'login.html', {"form": form})


def logout_page(request):
    logout(request)
    return redirect('/login')
