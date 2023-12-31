from django.urls import path
from .views import (
    CreateMeeting,
    DeleteMeeting,
    JoinMeeting,
    LeaveMeeting,
    ChangeMeetingStatus,
    MeetingSearchView,
    MeetingDetailView,
    JoinMeetingRoom,
    LeaveMeetingRoom,
    MeetingListView,
    IsMemberView,
    EvaluateMemberView,
    ChangMeetingContents,
    NotificationListCreateView,
    NotificationRetrieveUpdateDestroyView,
)

app_name = 'quickmatch'

urlpatterns = [
    # 모임 만들기
    path('create/', CreateMeeting.as_view(), name='create'),

    # 모임 삭제
    path('<int:quickmatchId>/delete/', DeleteMeeting.as_view(), name='delete'),

    # 모임 참석
    path('join/<int:quickmatchId>/', JoinMeeting.as_view(), name='join'),
    
    # 모임 떠나기
    path('leave/<int:quickmatchId>/', LeaveMeeting.as_view(), name='leave'),

    # 모임 상태 변경
    path('<int:quickmatchId>/status/', ChangeMeetingStatus.as_view(), name='status'),
    
    # 모임 내용 수정
    path('<int:quickmatchId>/contents/', ChangMeetingContents.as_view(), name='status'),

    # 모임 전체 목록 보기
    path('list/', MeetingListView.as_view(), name='list'),

    # 모임 검색
    path('search/', MeetingSearchView.as_view(), name="search"),
    
    # 모임 목록
    path('list/', MeetingListView.as_view(), name='list'),

    # 모임 디테일
    path('<int:quickmatchId>/detail/', MeetingDetailView.as_view(), name='meeting-detail'),
    
    # 모임 채팅 참가 DB 반영
    path('<int:quickmatchId>/detail/joinchat/', JoinMeetingRoom.as_view(), name='meeting-chat-join'),
    
    # 모임 채팅 떠나기 DB 반영
    path('<int:quickmatchId>/detail/leavechat/', LeaveMeetingRoom.as_view(), name='meeting-chat-leave'),

    # 모임 멤버 여부 확인
    path('is_member/<int:meeting_id>/', IsMemberView.as_view(), name='is_member'),

    # 모임 맴버 평가
    path('evaluate_member/<int:member_id>/<int:meeting_id>/', EvaluateMemberView.as_view(), name='evaluate_member'),

    # 모든 알림 가져오기 및 생성
    path('notifications/', NotificationListCreateView.as_view(), name='list-create-notifications'),

    # 특정 알림 상세정보 수정 및 삭제
    path('notifications/<int:pk>/', NotificationRetrieveUpdateDestroyView.as_view(), name='retrieve-update-notification'),
]
