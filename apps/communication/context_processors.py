def navigation_counts(request):
    if not request.user.is_authenticated:
        return {'unread_notifications':0,'unread_messages':0}
    return {
        'unread_notifications': request.user.notifications.filter(is_read=False).count(),
        'unread_messages': request.user.conversations.filter(messages__is_read=False).exclude(messages__sender=request.user).distinct().count(),
    }
