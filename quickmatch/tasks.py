from celery import shared_task
from . import models

@shared_task
def enable_user_evaluation(meeting_id):
    meeting = models.Meeting.objects.get(pk=meeting_id)
    meeting.can_evaluate = True
    meeting.save()

    for member in meeting.meeting_member.all():
        models.Notification.objects.create(user=member, message='회원을 평가할 수 있습니다!')
