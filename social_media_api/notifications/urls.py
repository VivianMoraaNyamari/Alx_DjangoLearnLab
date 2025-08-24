from django.urls import path
from .views import NotificationListView

urlpatterns = [
    # This URL will list all of a user's notifications.
    path('', NotificationListView.as_view(), name='notification_list'),
]
