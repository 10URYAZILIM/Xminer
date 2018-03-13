from django.shortcuts import render,HttpResponse,redirect
from .forms import UpdateUserForm
def home(request):
    return render(request,'index.html')

def index(request):
    if not request.user.is_authenticated:
        return redirect('home')
    context = {
        'link': 'index'
    }
    return render(request,'app/index.html',context)

def user(request):
    if not request.user.is_authenticated:
        return redirect('home')

    ## UPDATE FORMUNU OLUŞTURALIM
    form=UpdateUserForm(instance=request.user)
    context={
        'link':'user',
        'form':form
    }
    return  render(request,'app/user.html',context)

