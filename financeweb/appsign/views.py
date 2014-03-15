#-!- coding:utf-8 -!-
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _
from django.views.generic.base import View
from django.http import HttpResponseRedirect, HttpResponse
from financeweb.apphome import models
class SignInView(View):
    model = models.User
    template_name = "appsign/signin.html"
    
    def get(self, request):
        return render_to_response(self.template_name, {})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        from django.contrib.auth import authenticate
        from django.contrib.auth import login
        user = authenticate(username=username, password=password) 
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("home")) # Success
            else:
                return HttpResponse(_(u"用户已被禁用！"))
        else:
            return HttpResponse(_(u"用户名或密码不正确"))


class SignOutView(View):
    def get(self, request):
        from django.contrib.auth import logout
        logout(request)
        return HttpResponseRedirect(reverse("home"))
