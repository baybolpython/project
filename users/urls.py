from django.urls import path
from .views import (
    endreg,
    Authorization_api_view,
    register_api_view,



)



urlpatterns = [
    path('authorization/', Authorization_api_view.as_view(), name='authorization'),
    path('register/', register_api_view, name="register"),
    path('activation_code_form/', endreg, name="endreg"),
]