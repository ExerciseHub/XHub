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
        print(qdict)
        data = qdict.items()
        
        print(data)
        serializer = MeetingSerializer(data=data)
        # print(serializer)
        print(serializer.is_valid())
        # serializer.organizer = request.user
        if serializer.is_valid():
            
            print(serializer.data)
            meeting = serializer.create()
            print(meeting)
            # meeting.save()
            return Response({"data": "valid"}, status=status.HTTP_200_OK)
        
        return Response({"message": "data is not available"})


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