from django.shortcuts import redirect, render
from .models import Item, List
from .forms import ItemForm, ExistingListItemForm, CustomAuthenticationForm
from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, FormView, RedirectView

# from .forms import UserCreationForm, CustomAuthenticationForm


# Create your views here.
def home_page(request):
    return render(request, 'home.html', {"form": ItemForm()})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, "form": form})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form": form})


class LoginView(FormView):

    form_class = CustomAuthenticationForm
    success_url = '/'
    template_name = 'login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)



