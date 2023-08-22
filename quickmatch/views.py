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
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({"message": "get method is not available."})
    
    def post(self, request):
        qdict = request.data
        serializer = MeetingSerializer(data=qdict)
        
        if serializer.is_valid():
            
            data = serializer.data
            quickmatch = serializer.create(data) # 오브젝트 생성만
            quickmatch.organizer = request.user
            
            category_list = [i[0] for i in Meeting.CATEGORY_CHOICE]
            gender_list = [i[0] for i in Meeting.GENDER_CHOICE]
            status_list = [i[0] for i in Meeting.STATUS_CHOICE]
            
            # 카테고리, 성별제한, 상태 default설정. (목록에 없는 값은 is_valid False)
            if not data.get('category', None):
                quickmatch.category = category_list[0]
                
            if not data.get('gender_limit', None):
                quickmatch.category = gender_list[2]
                
            if not data.get('status', None):
                quickmatch.status = status_list[0]

            quickmatch.save() # 오브젝트 저장
            return Response({"message": "create sucess!", "meeting": repr(quickmatch)}, status=status.HTTP_200_OK)
        
        return Response({"message": "data is not available", "error": serializer.errors})


class DeleteMeeting(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, quickmatchId):
        return Response({"message": "GET method is not available."})
    
    def post(self, request, quickmatchId):
        
        quickmatch = get_object_or_404(Meeting, pk=quickmatchId)
        if quickmatch.organizer==request.user:
            result = {"message": "meeting deleted!",
                        "meeting": repr(quickmatch),}
            quickmatch.delete()
            return Response(result, status=status.HTTP_200_OK)
        
        return Response({"message": "Meeting is not exists"}, status=status.HTTP_404_NOT_FOUND)
    

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