from  django.urls import  path
from . import views
urlpatterns = [
    path('',views.toLogin_view),
    path('index/',views.Login_view),
    path('toregister/',views.toregister_view),
    path('register/',views.register_view),
    path('upload/', views.upload_students, name='upload_students'),
    path('roll_call/', views.roll_call, name='roll_call'),
    path('confirm_roll_call/', views.confirm_roll_call, name='confirm_roll_call'),  # 确认点名
]