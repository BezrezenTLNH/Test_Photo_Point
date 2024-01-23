from django.urls import path

from currency_app.current_usd import views

urlpatterns = [
    path('', views.get_current_usd),
]
