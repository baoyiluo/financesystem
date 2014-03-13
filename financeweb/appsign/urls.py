from django.conf.urls import patterns, include, url
import views
urlpatterns = patterns(
    '',
    url(r'^signin/$', views.SignInView.as_view(), name="signin"),
    url(r'signout/$', views.SignOutView.as_view(), name="signout"),
)
