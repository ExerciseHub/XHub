from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from .tasks import enable_user_evaluation

User = get_user_model()

# Create your models here.
class Meeting(models.Model):
    title = models.CharField(max_length=100)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    description = models.TextField(blank=True, null=True)
    age_limit = models.DateField(blank=True, null=True)
    rating = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    CATEGORY_CHOICE = (("축구(풋살)", "축구(풋살)"), ("농구", "농구"), ("배트민턴", "배트민턴"), ("볼링", "볼링"), ("테니스", "테니스"), ("골프", "골프"))
    category = models.CharField(choices=CATEGORY_CHOICE, max_length=50, blank=True, null=True)
    
    GENDER_CHOICE = (("M", "남"), ("W", "여"), ("X", "무관"))
    gender_limit = models.CharField(choices=GENDER_CHOICE, max_length=50, default="X")
    
    STATUS_CHOICE = (("모집중", "모집중"), ("모집완료", "모집완료"), ("취소", "취소"))
    status = models.CharField(choices=STATUS_CHOICE, max_length=50, default="모집중")

    location = models.CharField(max_length=255)  # 고민
    # 참여자
    meeting_member = models.ManyToManyField(User, through='MeetingMembers', related_name='quickmatches', blank=True)  # 고민

    max_participants = models.PositiveIntegerField()
    current_participants = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)

    can_evaluate = models.BooleanField(default=False)

    def __repr__(self):
        return f"{self.id}:{self.title}-{self.description}-{self.created_at}"
    
    def __str__(self):
        return f"{self.id}:{self.title}-{self.description}-{self.created_at}"
    
    def add_participant(self):
        if self.current_participants < self.max_participants:
            self.current_participants += 1
            self.save()

    def remove_participant(self):
        if self.current_participants > 1:
            self.current_participants -= 1
            self.save()

    def save(self, *args, **kwargs):
        if self.pk:
            orig = Meeting.objects.get(pk=self.pk)
            if orig.status != self.status and self.status == "모집완료":
                # 30분 뒤에 enable_user_evaluation 태스크를 스케줄링
                enable_user_evaluation.apply_async(args=[self.pk], countdown=5 * 60)  # 5분 * 60초
        super(Meeting, self).save(*args, **kwargs)


class MeetingMembers(models.Model):
    quickmatch = models.ForeignKey('Meeting', on_delete=models.CASCADE)
    attendant = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"meeting:{self.quickmatch.id} , user:{self.attendant.id}"
    
    def __repr__(self):
        return f"meeting:{self.quickmatch} , user:{self.attendant}"


class MeetingRoom(models.Model):
    name = models.CharField(max_length=255)
    meeting = models.OneToOneField('Meeting', on_delete=models.CASCADE)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rooms")
    current_users = models.ManyToManyField(User, related_name="current_rooms", blank=True)
    
    def __str__(self):
        return f'id: {self.id}, name: {self.name}, host:{self.host}'


class MeetingMessage(models.Model):
    room = models.ForeignKey("MeetingRoom", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.room.id}-({self.user.id}) : {self.content}"


class UserEvaluation(models.Model):
    evaluator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="given_evaluations")
    evaluated = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_evaluations")
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    is_positive = models.BooleanField()  # Y면 True, N이면 False
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("evaluator", "evaluated", "meeting")
