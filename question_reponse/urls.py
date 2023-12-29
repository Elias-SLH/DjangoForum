from django.urls import path

from . import views

app_name = 'qr'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('question/new/', views.ask_question, name='ask_question'),
    path('question/<int:pk>/', views.QuestionDetailView.as_view(), name='detail'),
    path('vote/<int:pk>/', views.vote, name='vote'),
    path('search/', views.search, name='search'),
    path('profile/', views.profile, name='profile'),
    path('question/edit/<int:pk>/', views.UpdateQuestion.as_view(), name='edit_question'),
    path('question/delete/<int:pk>/', views.DeleteQuestion.as_view(), name='delete_question'),
    path('answer/edit/<int:pk>/', views.UpdateAnswer.as_view(), name='edit_answer'),
    path('answer/delete/<int:pk>/', views.DeleteAnswer.as_view(), name='delete_answer'),
    path('profile/disable/<int:pk>/', views.disable_user, name='disable_user'),
]
