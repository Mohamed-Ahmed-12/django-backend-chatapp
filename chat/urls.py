from django.urls import path 
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()

# Correct registration - remove .as_view()
router.register("rooms", views.RoomViewset, basename="room")
router.register("messages", views.TextMessageViewset, basename="message")

urlpatterns = [
    path('user/<int:user_id>/rooms/', views.get_user_rooms, name='user_rooms'),
    path('languages/', views.get_languages, name='get_languages'),
]+router.urls