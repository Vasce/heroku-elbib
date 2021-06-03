from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponse
from django.views import generic

from .models import Content, Favorite
from django.db.models import Q


# Create your views here.

def add_to_favorite(request, pk):
    if Favorite.objects.filter(user=request.user, favorite=pk).exists():
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    content = get_object_or_404(Content, pk=pk)
    fav = Favorite.objects.create(user=request.user, favorite=content)
    fav.save()
    # fav.favorite.add(content)
    return  HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_from_favorite(request, pk):
    Favorite.objects.filter(id=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    

class SignInView(View):
    def get(self, request):
        return render(request, "signin.html")

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)

            return redirect(reverse("main")) #render(request, "page.html")
        else:
            return render(request, "signin.html")


class SignUpView(View):
    def get(self, request):
        return render(request, "signup.html")
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        pass_retry = request.POST['pass_retry']
        if not(username and password and pass_retry):
            request.err = 'empty'
        elif User.objects.filter(username=username).exists():
            request.err = 'user_exists'
            request.exiting_user = username
        elif pass_retry != password:
            request.err = 'wrong_retry'
        elif not self.weak_password(password):
            request.err = 'weak_pass'
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect(reverse("main"))
        return render(request, "signup.html")
    
    def weak_password(self, pass_string):
        print(len(pass_string))
        if len(pass_string) < 8:
            return 1
        return 0

class MainView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if 'search_string' not in request.GET:
                return render(request, "main.html")
            else:
                search_string = request.GET['search_string']
                return render(request, 'page.html',)
        else:
            return redirect(reverse("signin"))

class PageView(generic.ListView):
    model = Content
    context_object_name = 'page'
    template_name = 'page.html'
    def get_queryset(self):
        query = self.request.GET.get('search_string')
        if query == None or query == '':
            return None
        return Content.objects.filter(Q(author__icontains=query) | Q(title__icontains=query))


class PoiskView(View):
    model = Content
    def get(self, request):
        return render(request, "poisk.html")


class SpravkaView(View):
    def get(self, request):
        return render(request, "spravka.html")


class FavoriteView(generic.ListView):
    model = Favorite
    context_object_name = 'Favorite'
    template_name = 'favorite.html'
    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
    # def get(self, request):
    #     return render(request, "favorite.html")