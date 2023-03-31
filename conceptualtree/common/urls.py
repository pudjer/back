from django.urls import path

from common.views import UserView

urlpatterns = [
    path('user/', UserView.as_view())


]