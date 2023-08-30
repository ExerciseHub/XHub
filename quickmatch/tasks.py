from celery import shared_task
from .models import Meeting

@shared_task
def enable_user_evaluation(meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id)
    meeting.can_evaluate = True
    meeting.save()
