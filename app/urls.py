from django.urls import path
from .views import (
    index,
    # list_api_view,
    detail_api_view,
    AppStorView,
    ApplistView,
    # AppStorDetailView,
)

urlpatterns = [
    path('index/', index, name='index'),
    # path('app_list/', list_api_view, name='app_list'),
    path('app_detail/<int:id>/', detail_api_view, name='app_detail'),

    path('appstors/', AppStorView.as_view({
        'get': 'list',
        'post': 'create'
    }), name='appstor'),
    path('app_stors/<int:id>', AppStorView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('app_class/', ApplistView.as_view(), name='app')
]