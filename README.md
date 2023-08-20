# XHub
단체 스포츠 모임 플랫폼 (Team sports gathering platform)

## Code Convention(삭제 예정)
### Code lay-out
- 들여쓰기(indent)
    - class 별 2칸
    - class내 method 별 1칸

### Comments
- 주석(Docstring)을 작성할 때는 기존 코드에서 2칸을 띄고, # 에서 한칸 띄고 작성합니다.
    - `age = 30  # 주석`
### Naming Conventions
- 클래스 명은 파스칼케이스(PascalCase)로 작성합니다.
- 함수명과 변수명은 스네이크케이스(snake_case)로 작성합니다.


## 브랜치 전략(삭제 예정)
- 배포 브랜치: main
- 개발 브랜치: develop
    - 배포 전 기능 테스트 브랜치
- 기능 개발 브런치 : appname-function
    - ex) player-logout, quickmatch-create ...
    - 기능 개발 브랜치 완료 시 개발 브랜치(develop) 으로 merge


## 개발환경
- Python 3.10+
- python-decouple 3.8
- Django 4.2+
- DRF  3.14.0
- DRF-simplejwt 5.2+
- swagger-ui-py 22.7+
- psycopg2 2.9+
<!--  MAC : install psycopg2-binary -->
그 외 requirements.txt 참고 부탁드립니다.

## 배포환경
- Amazon
    - ECS
    - EC2
    - Lightsail

- Nginx
- uWSGI OR gunicorn


## 폴더트리

## ERD
![ERD](asset/image.png)

기능 별 테이블 구분
- player
    - User
    - DirectChatting
- quickmatch
    - Meeting
    - MeetingChat
- board
    - Post
    - Comment
    