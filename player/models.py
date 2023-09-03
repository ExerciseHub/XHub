from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        이메일과 비밀번호로 사용자를 생성하고 반환합니다.
        """
        if not email:
            raise ValueError("이메일 필드는 반드시 설정되어야 합니다.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        이메일과 비밀번호로 슈퍼유저를 생성하고 반환합니다.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=200, unique=True)
    activity_point = models.PositiveIntegerField(default=0)

    # Profile
    nickname = models.CharField(max_length=100)
    profile_img = models.ImageField(upload_to='images/profile/', blank=True, null=True)
    age = models.DateField(blank=True, null=True)
    
    GENDER_CHOICE = (("M", "남"), ("W", "여"), ("X", "비공개"))
    gender = models.CharField(choices=GENDER_CHOICE, max_length=50, blank=True, null=True)

    CATEGORY_CHOICE = (("축구(풋살)", "축구(풋살)"), ("농구", "농구"), ("배트민턴", "배트민턴"), ("볼링", "볼링"), ("테니스", "테니스"), ("골프", "골프"))
    category = models.CharField(choices=CATEGORY_CHOICE, max_length=50, blank=True, null=True)

    POSITION_CHOICE = (("FW", "공격"), ("DF", "수비"), ("SUB", "보조"), ("X", "비활성화"))
    position = models.CharField(choices=POSITION_CHOICE, max_length=100, blank=True, null=True)

    height = models.PositiveIntegerField(blank=True, null=True)
    weight = models.PositiveIntegerField(blank=True, null=True)
    location = models.CharField(blank=True, null=True)  # 지역, 고민중
    
    friend = models.ManyToManyField("self", blank=True, symmetrical=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()  # 재정의된 매니저 클래스 추가

    USERNAME_FIELD = "email"  # 고유 식별자로 이메일 사용
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []  # 이제 기본적으로 이메일이 필요하므로 이 목록에서 제거


class DMRoom(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True, unique=True)
    host = models.ForeignKey("User", on_delete=models.CASCADE, related_name="room")
    current_users = models.ManyToManyField(User, related_name="current_room", blank=True)

    def __str__(self):
        return f"Room({self.name} {self.host})"


class DirectMessage(models.Model):
    room = models.ForeignKey("DMRoom", on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="messages")
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message({self.user} {self.room})"
