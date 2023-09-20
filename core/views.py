# 테스트용 - welcome page (진입 시 보일 화면)
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to Xhub API server")
