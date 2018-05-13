from django.urls import path
from . import views


urlpatterns = [
    path('item/', views.ItemViewSet.as_view()),
    path('item/<int:pk>/', views.ItemDetail.as_view()),
    path('item/<int:pk>/<str:action>/<int:qty>', views.ItemAction.as_view()),
]
