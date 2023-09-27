# XHub
단체 스포츠 모임 플랫폼 (Team sports gathering platform)


## 프로젝트 개요
- XHub는 단체운동을 하고 싶은 개인들이 모여 같이 운동을 즐길 수 있는 Hub역할의 서비스입니다.
- 좋아하지만 혼자서 즐기지 못하는 축구, 농구, 배드민턴 등의 운동들을 지역 주민들과 같이 즐길 수 있는 서비스입니다.
- 1회성 운동 모임을 하며, 마음이 잘 맞는 다른 사용자를 친구 추가하여 대화를 할 수도 있습니다.
- 1회성 운동 모임이 끝나면 사용자의 활동 점수에 영향이 가는 2중 선택지 평가를 하여, 매너 사용자와 비매너 사용자를 확인할 수도 있습니다.
- 1회성 운동 모임으로 운동도 즐길 수 있고, 게시판에서 운동에 관한 건강한 정보를 공유할 수도 있습니다.


## 기여자
| 기여자 | 깃헙링크              |
|-------|---------------------|
| 김종완 | [Link](https://github.com/mireu-san) |
| 민성철 | [Link](https://github.com/AMinSC) |
| 유진수 | [Link](https://github.com/YuJinsoo) |


## 구동 방식
- Windows : PowerShell 로 실행
- Mac : zsh 로 실행

```
사전작업:
- git clone 으로 본 repository 의 main branch 를 받습니다.

최초 실행 시,
- docker compose up --build -d
- docker compose run django python manage.py collectstatic
- docker compose run django python manage.py makemigrations
- docker compose run django python manage.py migrate

이 후 실행 시,
docker compose up -d
```

## 테스트 계정
- email: `xhubadmin@example.com`
- password : `xhubpw123`
- http://54.248.217.183/admin 


## 개발 기간
- 2023.08 ~ 2023.10 (1.5개월)
- 기획, 테스트, 클라이언트 개발을 포함한 기간입니다.


## 개발환경
- python:3.11.4-alpine3.18
- python-decouple 3.8
- Django 4.2+
- DRF 3.14+
- DRF-simplejwt 5.2+
- drf-yasg==1.21+
- swagger-ui-py 22.7+
- psycopg2 2.9+
- celery 5.3+
- channels 4.0+
- channels-redis 4.1+
- daphne 4.0+
- flake8 6.1+
- Pillow 10.0+
- Docker

그 외 설치된 패키지는 requirements.txt 를 참고 부탁드립니다.


## 배포환경
- Amazon Web Server
    - Lightsail
    - Ubuntu 22.04, 2 vCPU, 2G(RAM), 60 GB SSD
- Docker
  - 필요 부분들을 docker container로 만들고 `docker compose` 명령어를 이용해 한 번에 설치가 가능하도록 구성
  - 도커허브 이미지로 배포
- 웹서버
  - Nginx
  - Django WSGI: gunicorn
  - Django ASGI: daphne


## 프로젝트 구성도
![Alt text](asset/system.png)
- Web 서버로 NginX
- HTTP와 Websocket을 처리하는 서버를 gunicorn과 daphne로 따로 구성
- player, quickmatch, board 앱으로 구성되어있고, 프로젝트 앱은 core 입니다.
- player와 quickmatch에는 실시간 채팅 기능을구현하기 위해 consumers.py 가 있습니다.
- channels_jwt_auth_middleware 폴더는 채팅 기능에서 jwt인증을 위해 필요한 미들웨어 입니다.


## 프로젝트 흐름도
![Alt text](asset/flowchart.png)


## ERD
![Alt text](asset/image.png)

기능 별 테이블 구분
- player
    - User (사용자-프로필)
    - DMRoom (1:1 채팅방)
    - DirectMessage (1:1 채팅)
- quickmatch
    - Meeting (1회성 모임)
    - MeetingMember (1회성 모임 멤버)
    - MeetingChat (1회성 모임 채팅)
    - UserEvaluation (유저 평가)
    - Notification (유저 평가 알람)
- board
    - Post (게시판)
    - Comment (댓글)


## URL

- swagger 적용
- swagger Link : http://54.248.217.183/swagger/


## 라이센스
- MIT License
- 본 프로젝트는 상업적 용도로 사용되지 않습니다.


## 코드 컨벤션 (Code Convention)
### Code lay-out
- 줄 간격(indent)
    - class 별 2줄
    - class내 method 별 1줄

### Comments
- 주석(Docstring)을 작성할 때는 기존 코드에서 2칸을 띄고, # 에서 한칸 띄고 작성합니다.
    - `age = 30  # 주석`
    
### Naming Conventions
- 클래스 명은 파스칼케이스(PascalCase)로 작성합니다.
- 함수명과 변수명은 스네이크케이스(snake_case)로 작성합니다.

### Flake8, Black 적용
- .flake8


## 브랜치 전략
- 배포 브랜치: main
- 개발 브랜치: develop
    - 배포 전 기능 테스트 브랜치
- 기능 개발 브런치 : appname-function
    - ex) player-logout, quickmatch-create ...
    - 기능 개발 브랜치 완료 시 개발 브랜치(develop) 으로 merge
