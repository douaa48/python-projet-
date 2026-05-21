from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Notification

@login_required
def notifications_list(request):

    notifications = (

        Notification.objects
        .filter(user=request.user)
        .order_by('-created_at')

    )

    unread_count = notifications.filter(
        is_read=False
    ).count()

    context = {

        "notifications": notifications,

        "unread_count": unread_count,

    }

    return render(
        request,
        "frontend/notifications/list.html",
        context
    )
@login_required
def mark_as_read(request, id):

    notif = Notification.objects.filter(
        id=id,
        user=request.user
    ).first()

    if notif:

        notif.is_read = True

        notif.save()

    return redirect("notifications")

@login_required
def mark_all_read(request):

    Notification.objects.filter(

        user=request.user,
        is_read=False

    ).update(is_read=True)

    return redirect("notifications")