# -*- coding:utf-8 -*-
# Create your views here.
from django.utils.translation import ugettext as _
from django.views.generic.base import View
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from financeweb.apphome import models
from financeweb.apphome.views import auth_required

class ExamineMessages(View):
    model = models.Finance
    @auth_required
    def get(self, request, *args, **kwargs):
        financelist = self.model.objects.filter(status=0)
        count=0
        for finance in financelist:
            if request.user not in finance.examineperson.all():
                count+=1
        return HttpResponse(count)

class Index(View):
    template_name = 'appfinance/index.html'
    @auth_required
    def get(self, request):
        username = request.user.username
        objects = models.Finance.objects.all()
        return render_to_response(self.template_name, {'username': username, 'objects':objects})

class ExamineDate(View):
    template_name = 'appfinance/examinedatashow.html'
    model = models.Finance
    @auth_required
    def get(self, request, *args, **kwargs):
        username = request.user.username
        financelist = self.model.objects.filter(status=0)
        objects = []
        for finance in financelist:
            if request.user not in finance.examineperson.all():  
                objects.append(finance)
        return render_to_response(self.template_name, {'username': username,'objects':objects})

class ExaminemakeShow(View):
    template_name = 'appfinance/examinemakeshow.html'
    @auth_required
    def get(self, request, *args, **kwargs):
        financepk = request.GET.get('finance', '')
        operate = request.GET.get('operate', '')
        if financepk:
            try:
                financeobject = models.Finance.objects.get(pk=int(financepk))
                return render_to_response(self.template_name, {'financeobject':financeobject,'operate':operate})
            except:
                return HttpResponse(u'数据错误，申请单不存在')
        else:
            return HttpResponse(u'数据错误，申请单编号不能为空')
    def post(self, request, *args, **kwargs):
        user = request.user
        financepk = request.POST.get('finance', '')
        operate = request.POST.get('operate', '')
        info = request.POST.get('info', '')
        financeobject=models.Finance.objects.get(pk=int(financepk))
        if operate:
            status = True 
        else:
            status = False 
        if models.FinanceUser.objects.filter(user=user, finance=financeobject): 
            #import pdb; pdb.set_trace()
            financeuser=models.FinanceUser.objects.get(user=user, finance=financeobject)
            financeuser.status = status
            financeuser.examineinfo = info
            financeuser.save()
            if  models.FinanceUser.objects.filter(user=user, finance=financeobject,status=True) == 4:
                    financeobject.status = 1 
            elif models.FinanceUser.objects.filter(user=user, finance=financeobject,status=False):
                    financeobject.status = -1 
            financeobject.save()
        else:
            financeuser = models.FinanceUser(user=user, finance=financeobject, status=status, examineinfo=info)
            financeuser.save()
            if  len(models.FinanceUser.objects.filter(user=user, finance=financeobject,status=True)) == 4:
                    financeobject.status = 1 
            elif models.FinanceUser.objects.filter(user=user, finance=financeobject,status=False):
                    financeobject.status = -1 
            financeobject.save()
        return HttpResponse(u'审批成功')
