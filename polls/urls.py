from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.userlogout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.PasswordChange.as_view(), name='password_change'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
    path('questions/', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('create_question/', views.create_question, name='create_question'),
]