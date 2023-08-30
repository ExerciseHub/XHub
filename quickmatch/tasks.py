from celery import shared_task
from . import models

@shared_task
def enable_user_evaluation(meeting_id):
    meeting = models.Meeting.objects.get(pk=meeting_id)
    meeting.can_evaluate = True
    meeting.save()
