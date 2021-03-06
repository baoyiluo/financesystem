# -*- coding:utf-8 -*-
# Create your views here.
from django.utils.translation import ugettext as _
from django.views.generic.base import View
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from financeweb.apphome import models
from django.core.urlresolvers import reverse
from financeweb.apphome.views import auth_required

class ExamineMessages(View):
    model = models.Finance
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
        user = request.user
        username = user.username
        objects = models.Finance.objects.all()
        return render_to_response(self.template_name, {'username': username, 'objects':objects})

class SelfFinance(View):
    template_name = 'appfinance/selffinance.html'
    @auth_required
    def get(self, request):
        user = request.user
        username = user.username
        objects = models.Finance.objects.filter(startperson=user)
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

class ExamineHistroyDate(View):
    template_name = 'appfinance/examinehistoryshow.html'
    @auth_required
    def get(self, request, *args, **kwargs):
        user = request.user
        objects = user.financeuser_set.all()
        return render_to_response(self.template_name, {'objects':objects})

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
            financeuser=models.FinanceUser.objects.get(user=user, finance=financeobject)
            financeuser.status = status
            financeuser.examineinfo = info
            financeuser.save()
            if  len(models.FinanceUser.objects.filter(finance=financeobject,status=True)) == 4:
                    financeobject.status = 1 
            elif models.FinanceUser.objects.filter(finance=financeobject,status=False):
                    financeobject.status = -1 
            else:
                    financeobject.status = 0 
            financeobject.save()
        else:
            financeuser = models.FinanceUser(user=user, finance=financeobject, status=status, examineinfo=info)
            financeuser.save()
            if  len(models.FinanceUser.objects.filter(finance=financeobject,status=True)) == 4:
                    financeobject.status = 1 
            elif models.FinanceUser.objects.filter(finance=financeobject,status=False):
                    financeobject.status = -1 
            else:
                    financeobject.status = 0 
            financeobject.save()
        return HttpResponse(u'审批成功')

class MakeFinance(View):
    template_name="appfinance/makefinance.html"
    @auth_required
    def get(self, request, *args, **kwargs):
        financetypelist=["-1"]
        financepk = request.GET.get('financepk','')
        if financepk:
            try:
                financeobject = models.Finance.objects.get(pk=int(financepk))
                financename = financeobject.financename
                financeinfo = financeobject.financeintro
                financecount = financeobject.maneycount
                financetype = financeobject.financetype
            except:
                financename = ""
                financeinfo = ""
                financecount = ""
                financetype = "-1"
        else:
            financename = ""
            financeinfo = ""
            financecount = ""
            financetype = "-1"
        context={
            'financepk':financepk,
            'financename':financename,
            'financeinfo':financeinfo,
            'financetypelist':financetypelist,
            'financetype':financetype,
            'financecount':financecount

        }
        return render_to_response(self.template_name,context) 
    @auth_required
    def post(self, request, *args, **kwargs):
        financename = request.POST.get('financename','')
        financeinfo = request.POST.get('financeinfo','')
        financetype = request.POST.get('financetype','')
        financecount = request.POST.get('financecount','')
        financepk = request.POST.get('financepk','')
        try:
            float(financecount)
        except:
            return HttpResponse(u"金额必需是浮点数或整数")
        if financename and financeinfo and financetype and financecount:
            user = request.user
            if financepk:
                newobject = models.Finance.objects.get(pk=int(financepk))
                financeuserlist = newobject.financeuser_set.all()
                for financeuser in financeuserlist:
                    financeuser.delete()
                newobject.maneycount = financecount
                newobject.financename = financename
                newobject.financeintro = financeinfo
                newobject.financetype = financetype
                newobject.status = 0 
            else:
                newobject = models.Finance(startperson=user, maneycount=financecount, financename=financename, financeintro=financeinfo, financetype=financetype)
            newobject.save()
            return HttpResponseRedirect(reverse("home"))
        else:
            return HttpResponse(u'名称:'+financename+u' 描述:'+financeinfo+u'类型:'+financetype+u'金额:'+financecount+u" 都不能为空,且金额为浮点型")
