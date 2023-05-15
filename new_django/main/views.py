from django.shortcuts import render, redirect
from .models import Users, Skins, History, Case, Support
from .forms import UsersForm, UsersLogin, SupportForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


#1kam
#12345

def get_cookies(key, request):
    if key in request.COOKIES:
        return request.COOKIES[key]
    else:
        return ""

def index(request):
    top = History.objects.order_by('-coef')[:10]
    win_hist = History.objects.order_by('-time')[:10]
    cases = Case.objects.order_by('price')[:]
    for i in cases:
        i.image = str(i.image)[12:]
    username = get_cookies('username', request)
    if username == "":
        return render(request, "main/case.html", {'top': top, 'win_hist': win_hist, 'username': username, 'cases': cases})
    else:
        user = Users.objects.filter(name=username).order_by('name')[0]
        return render(request, "main/case.html", {'top': top, 'win_hist': win_hist, 'username': username, 'user': user, 'cases': cases})

def support(request):
    error = ""
    username = get_cookies('username', request)
    if request.method == "POST":
        sup_user = Support()
        if username == "":
            error = "Авторизуйтесь, чтобы задать вопрос."
        else:
            sup_user.user_id = username
            sup_user.name = request.POST.get('name')
            sup_user.email = request.POST.get('email')
            sup_user.problem = request.POST.get('problem')
            sup_user.save()
    form = SupportForm()
    if username == "":
        return render(request, "main/support.html", {'username': username, 'form': form})
    else:
        user = Users.objects.filter(name=username).order_by('name')[0]
        return render(request, "main/support.html", {'username': username, 'user': user, 'form': form})

def my_acc(request):
    top = History.objects.order_by('-coef')[:10]
    win_hist = History.objects.order_by('-time')[:10]
    username = get_cookies('username', request)
    if username == "":
        return redirect("main:login")
    else:
        user = Users.objects.filter(name=username).order_by('name')[0]
        inv_items = []
        if user.inventory != "":
            inv = user.inventory.split(';')
            inv = list(map(int, inv))
            for i in inv:
                try:
                    el = Skins.objects.filter(skin_id=i).order_by('skin_id')[0]
                    el.image = str(el.image)[12:]
                    inv_items.append(el)
                except:
                    pass
        return render(request, "main/my_acc.html", {'top': top, 'win_hist': win_hist, 'username': username, 'user': user, 'inv_items': inv_items})
    
def register(request):
    if request.method == "POST":
        user = Users()
        user.name = request.POST.get('name')
        user.email = request.POST.get('email')
        user.password = request.POST.get('password')
        user.money = 0
        user.ref_code = 4567
        user.save()
        return redirect('main:login')
    username = get_cookies('username', request)
    if username == "":
        form = UsersForm()
        return render(request, "main/register.html", {'form': form, 'username': username})
    else:
        return redirect('main:my_acc')

def login(request):
    error = ""
    if request.method == "POST":
        try:
            user = Users.objects.filter(name=request.POST.get('name')).order_by('name')[0]
            password = request.POST.get('password')
        except Exception:
            error = "Неверный логин или пароль"
        else:
            if user.password == password:
                url = reverse('main:my_acc')
                ret = HttpResponseRedirect(url)
                ret.set_cookie('username', request.POST.get('name'))
                return ret
            else:
                error = "Неверный логин или пароль"
    username = get_cookies('username', request)
    if username == "":
        form = UsersLogin()
        return render(request, "main/login.html", {'form': form, 'username': username, 'error': error})
    else:
        return redirect('main:my_acc')
    
def faq(request):
    username = get_cookies('username', request)
    if username == "":
        return render(request, "main/faq.html", {'username': username})
    else:
        user = Users.objects.filter(name=username).order_by('name')[0]
        return render(request, "main/faq.html", {'username': username, 'user': user})

def exit(request):
    url = reverse('main:login')
    ret = HttpResponseRedirect(url)
    ret.delete_cookie('username')
    return ret

@csrf_exempt
def get_case_items(request):
    if request.method == "POST":
        case = Case.objects.filter(id=request.POST.get('id'))[0]
        case_items = case.items.split(';')
        skin_chance = dict()
        for i in case_items:
            i = i.split(':')
            skin_chance[i[0]] = i[1]
        skins_dict = dict()
        for i in skin_chance:
            item = Skins.objects.filter(skin_id=i)[0]
            skin_path = "/" + "/".join(str(item.image).split("/")[1:])
            skins_dict[item.skin_id] = {
                "name": item.name,
                "path": skin_path,
                "price": item.price,
                "quality": item.quality,
                "chance": skin_chance[i]
            }
        case_dict = {
            "case_id": case.id,
            "case_price": case.price,
            "case_items": skins_dict
        }    
        return JsonResponse(case_dict)
    
@csrf_exempt
def buy_case(request):
    username = get_cookies('username', request)
    if username == "":
        return JsonResponse({"status": "error", "status_descr": "user is not logged in"})
    else:
        user = Users.objects.filter(name=username).order_by('name')[0]
        case_price = float(request.POST.get('case_price'))
        if user.money - case_price >= 0: 
            user.money -= case_price
            user.save()
            return JsonResponse({"status": "success", "status_descr": "user is logged in", "balance": str(user.money)+'$'})
        else:
            return JsonResponse({"status": "error", "status_descr": "negative balance"})
        
@csrf_exempt
def inv_add_item(request):
    username = get_cookies('username', request)
    if username == "":
        return JsonResponse({"status": "error", "status_descr": "user is not logged in"})
    else:
        opened_item = request.POST.get('opened_item')
        user = Users.objects.filter(name=username).order_by('name')[0]
        user.inventory = opened_item + ';' + user.inventory
        user.save()
        history = History()
        history.user_id = username
        history.skin = request.POST.get('item_name')
        history.coef = round(float(request.POST.get('item_price')) / float(request.POST.get('case_price')), 1)
        history.time = datetime.now()
        history.save()
        return JsonResponse({"status": "success"})