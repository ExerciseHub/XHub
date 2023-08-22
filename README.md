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


## URL

|   앱 이름  |        기능        |                          URL                         | Method |   |
|:----------:|:------------------:|:----------------------------------------------------:|:------:|---|
| player     | 회원가입           | 도메인/player/register/                              | POST   |   |
|            | 로그인             | 도메인/player/login/                                 | POST   |   |
|            | 로그아웃           | 도메인/player/logout/                                | POST   |   |
|            | 회원수정           | 도메인/player/update/                                | POST   |   |
|            | 회원탈퇴           | 도메인/player/unregister/                            | POST   |   |
|            | 전체 회원조회      | 도메인/player/search/                                | GET    |   |
|            | 친구 조회          | 도메인/player/friends/                               | GET    |   |
|            | 친구 추가          | 도메인/player/add_friend/                            | POST   |   |
|            | 친구 삭제          | 도메인/player/rm_friend/<int:friend_id>/             | POST   |   |
|            | 활동점수           | 도메인/player/                                       |        |   |
|            | 친구와채팅         | 도메인/player/                                       |        |   |
|            | 그룹여부           | 도메인/player/                                       |        |   |
| quickmatch | 모임만들기         | 도메인/quickmatch/create/                            | POST   |   |
|            | 모임삭제           | 도메인/quickmatch/<int:quickmatchId>/delete/         | POST   |   |
|            | 모임참가           | 도메인/quickmatch/join/<int:quickmatchId>/           | POST   |   |
|            | 모임상태변경       | 도메인/quickmatch/<int:quickmatchId>/status/         | GET    |   |
|            | 회원평가           | 도메인/quickmatch/                                   |        |   |
|            | 모임만족도         | 도메인/quickmatch/                                   |        |   |
|            | 대화기능(그룹대화) | 도메인/quickmatch/                                   |        |   |
| board      | 게시글 조회(전체)  | 도메인/board/                                        | GET    |   |
|            | 게시글 생성        | 도메인/board/create/                                 | POST   |   |
|            | 게시글 상세보기    | 도메인/board/<int:board_id>/detail/                  | GET    |   |
|            | 게시글 삭제        | 도메인/board/<int:board_id>/delete/                  | POST   |   |
|            | 게시글 수정        | 도메인/board/<int:board_id>/update/                  | POST   |   |
|            | 게시글좋아요       | 도메인/board/<int:board_id>/like/                    | GET    |   |
|            | 댓글 달기          | 도메인/board/<int:board_id>/comment/write/           | POST   |   |
|            | 댓글 삭제          | 도메인/board/<int:board_id>/<int:comment_id>/delete/ | POST   |   |
|            | 댓글 수정          | 도메인/board/<int:board_id>/<int:comment_id>/edit    | PUT    |   |
|            | 댓글좋아요         | 도메인/board/<int:board_id>/<int:comment_id>/like/   | GET    |   |

