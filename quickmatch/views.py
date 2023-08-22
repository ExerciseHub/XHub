from django.shortcuts import render, get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Meeting, MeetingChat
from .serializers import MeetingSerializer

import io
from rest_framework.parsers import JSONParser


class CreateMeeting(APIView):
    # test를 위해 임시 AllowAny
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response({"message": "get method is not available."})
    
    def post(self, request):
        ## TODO - endpoint 작업
        qdict = request.data
        serializer = MeetingSerializer(data=qdict)
        
        # serializer.organizer = request.user
        if serializer.is_valid():
            
            data = serializer.data
            meeting = serializer.create(data) # 오브젝트 생성만
            meeting.organizer = request.user
            
            category_list = [i[0] for i in Meeting.CATEGORY_CHOICE]
            gender_list = [i[0] for i in Meeting.GENDER_CHOICE]
            status_list = [i[0] for i in Meeting.STATUS_CHOICE]
            
            # 카테고리, 성별제한, 상태 default설정. (목록에 없는 값은 is_valid Fail)
            if not data.get('category', None):
                meeting.category = category_list[0]
                
            if not data.get('gender_limit', None):
                meeting.category = gender_list[2]
                
            if not data.get('status', None):
                meeting.status = status_list[0]

            meeting.save() # 오브젝트 저장
            return Response({"data": "valid"}, status=status.HTTP_200_OK)
        
        return Response({"message": "data is not available", "error": serializer.errors})


class DeleteMeeting(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, quickmatchId):
        return Response({"message": "get is not developed yet."})
    
    def post(self, request, quickmatchId):
        
        quickmatch = get_object_or_404(Meeting, pk=quickmatchId)
        
        if quickmatch:
            return Response({"message": "meeting deleted!"})
        
        return Response({"message": "hahaha"})
    

class JoinMeeting(APIView):
    # test를 위해 임시 AllowAny
    permission_classes = [AllowAny]
    def get(self, request, quickmatchId):
        return Response({"message": "get is not developed yet."})
    
    def post(self, request, quickmatchId):
        
        quickmatch = get_object_or_404(Meeting, pk=quickmatchId)
        
        if quickmatch:
            return Response({"message": "meeting deleted!"})
        
        return Response({"message": "hahaha"})
    

class ChangeMeeting(APIView):
    # test를 위해 임시 AllowAny
    permission_classes = [AllowAny]
    def get(self, request, quickmatchId):
        return Response({"message": "get is not developed yet."})
    
    def post(self, request, quickmatchId):
        
        quickmatch = get_object_or_404(Meeting, pk=quickmatchId)
        
        if quickmatch:
            return Response({"message": "meeting deleted!"})
        
        return Response({"message": "hahaha"})