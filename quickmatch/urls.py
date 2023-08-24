from django.urls import path
from .views import CreateMeeting, DeleteMeeting, JoinMeeting, ChangeMeetingStatus, MeetingSearchView

app_name = 'quickmatch'

urlpatterns = [
    # 모임 만들기
    path('create/', CreateMeeting.as_view(), name='create'),

    # 모임 삭제
    path('<int:quickmatchId>/delete/', DeleteMeeting.as_view(), name='delete'),

    # 모임 참석
    path('join/<int:quickmatchId>/', JoinMeeting.as_view(), name='join'),

    # 모임 상태 변경
    path('<int:quickmatchId>/status/', ChangeMeetingStatus.as_view(), name='status'),

    # 모임 검색
    path('search/', MeetingSearchView.as_view(), name="search")
]
