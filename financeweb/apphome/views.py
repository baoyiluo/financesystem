# -*- coding:utf-8 -*-
# Create your views here.
from django.shortcuts import render_to_response
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
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
    template_name = 'index.html'
    @auth_required
    def get(self, request):
        username = request.user.username
        return render_to_response(self.template_name, {'username': username})
