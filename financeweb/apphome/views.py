# -*- coding:utf-8 -*-
# Create your views here.
from django.shortcuts import render_to_response
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import models
def auth_required(view):
    """"身份认证装饰器"""
    def decorator(self, request, *args, **kwargs):
        print args
        print '-------------------'
        print kwargs
        username = request.user.username 
        if username:
            return view(self, request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse("signin"))
    return decorator
class Index(View):
    @auth_required
    def get(self, request):
        return HttpResponseRedirect(reverse("home"))
