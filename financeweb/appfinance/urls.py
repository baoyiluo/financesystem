from django.conf.urls import patterns, include, url
import views
urlpatterns = patterns(
    '',
    #url(r'^signin/$', views.SignInView.as_view(), name="signin"),
    url(r'^getexaminemessages/$', views.ExamineMessages.as_view(), name="getexaminemessages"),
    url("^$", views.Index.as_view(), name="home"),
    url("^selffinance/$", views.SelfFinance.as_view(), name="selffinance"),
    url("^makefinance/$", views.MakeFinance.as_view(), name="makefinance"),
    url(r'^examineamekshow/$', views.ExaminemakeShow.as_view(), name="examinemakeshow"),
    url(r'^examineshow/$', views.ExamineDate.as_view(), name="examineshow"),
    url(r'^examinehistoryshow/$', views.ExamineHistroyDate.as_view(), name="examinehistoryshow"),
)
