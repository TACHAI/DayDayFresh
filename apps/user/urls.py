from django.conf.urls import url
from apps.user import views
from apps.user.views import register_view,ActiveView,LoginView
urlpatterns = [
    # url(r'^register$',views.register,name='register'),
    # url(r'^register_handle$',views.register_handle,name='register_hadle')
    url(r'^register',register_view.as_view,name='register'), #注册
    url(r'^active/(?P<token>.*)',ActiveView.as_view,name='active'), #激活
    url(r'^login$',LoginView.as_view,name='login'), #登录
]
