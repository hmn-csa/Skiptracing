from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import requests
import hashlib
from website.models import *
from django.http import Http404


# Create your views here.
def index(request):
   for i in list(request.session.keys()):
       if i != "":
           del request.session[i]
   if request.POST.get("username"):
      id = request.POST.get("username");
      pw = request.POST.get("password");
      pwmd5 = hashlib.md5(pw.encode()).hexdigest();
      re = requests.get(f'https://hmnflask-app.herokuapp.com/user/{id}-{pwmd5}');
      data = re.json()['result'];
      if data == "No such account":
          status = "User name / password is wrong";
          return render(request,'pages/home.html', {"status":status});
      else:
          if data['password'] == pwmd5:
              per = data['permission'];
              request.session['user'] = id;
              request.session['per'] = per;
              return redirect('/search');
   else:
      return render(request,'pages/home.html');
      
def search(request):
    if request.session.get('user'):
        username = request.session.get('user');
        if request.method == "POST":
            txt = request.POST.get("input");
            option = request.POST.get("option");
            if option == "ID no":
                re = requests.get(f'https://hmnflask-app.herokuapp.com/{txt}');
                data = re.json()['result'];
                if data == "No such name":
                  status = "ID no not found";
                  return render(request,'pages/search.html',{'status':status});
                else:
                  request.session['data'] = data;
                  return redirect('/search/view');
        else:
           return render(request,'pages/search.html',{'user':username});
    else:
        return redirect('/');
    


def overview(request):
    if request.session.get('user'):
        username = request.session.get('user');
        per = request.session.get('per');
        if request.POST.get('inputcard') :
            phone = request.POST.get('inputphone');
            card = request.POST.get('inputcard');
            if phone != "":
                re = requests.get(f'https://hmnflask-app.herokuapp.com/{phone}');
                data = re.json()['result'];
                if data == "No such name":
                    status = "Phone no not found";
                    return render(request,'pages/search.html',{'status':status});
                else:
                    request.session.modified = True;
                    request.session['data'] = data;
                    request.session.modified = True;
            else:
                re = requests.get(f'https://hmnflask-app.herokuapp.com/{card}');
                data = re.json()['result'];
                if data == "No such name":
                    status = "ID no not found";
                    return render(request,'pages/search.html',{'status':status});
                else: 
                    request.session.modified = True;
                    request.session['data'] = data; 
                    request.session.modified = True;
            
        else:
            data = request.session.get("data");
        contracts = 2;
        return render(request,'pages/overview.html',{'user':username,'data':data,'contract':contracts});        
    else:
        return redirect('/');


def customer(request):
    return render(request,'pages/customer.html');

def graph(request):
    return render(request,'pages/network_graph.html');

def geo(request):
    return render(request,'pages/geo_location.html');

def score(request):
    return render(request,'pages/score.html');


def error(request, exception):
    return render(request, 'pages/error404.html', {'message': exception})
