from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'helloengineer'

urlpatterns = [
    path('', views.index, name='index'),
    path('group_list/', views.GroupList.as_view(), name='group_list'),
    path('group_create/', views.GroupCreate, name='group_create'),
    path('group_thread/<int:pk>/', views.ThreadView.as_view(), name='group_thread'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name="helloengineer/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page="helloengineer:index"), name='logout'),
    path('userpage/<int:user_pk>/', views.userpage, name='userpage'),
    path('mypage/<int:user_pk>/', views.mypage, name='mypage'),
    path('profileupdate/<int:pk>/', views.profileupdate, name='profileupdate'),
    path('delete/<int:group_pk>/', views.delete_group, name='delete'),
]
