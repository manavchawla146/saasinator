from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.index, name="index"),
    path("submit-idea/", views.submit_idea, name="submit_idea"),
    path("history/", views.history, name="history"),
    path("history/<int:history_id>/", views.get_history_detail, name="history_detail"),
]
