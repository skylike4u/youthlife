# DRF APIView (ViewSet)
# from rest_framework.decorators import api_view
import jwt
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, NotFound
from .serializers import PrivateUserSerializer, PublicUserSerializer
from .models import User

"""
@api_view()
def test(request):
    all_users = User.objects.all()
    print(all_users)
    serializer = TestSerializer(all_users, many=True)
    return Response(serializer.data)
"""


class Me(APIView):
    """private URL"""

    # /me가 로그인한 user의 정보는 private해야 할 것 같음
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        # user랑 user가 보낸 데이터가 필요해. / partial도 True로 해주고.
        serializer = PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            # 새로운 user를 넘겨줄거야
            user = serializer.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data)


# create users API
# user를 만들 때 password도 함께 만들면 password가 Django authentication(인증) 시스템에서 작동함 - 우리가 한건 set_password 뿐임(간단하지)
class Users(APIView):
    def post(self, request):
        # is_valid를 하기 전에 password가 있는지 없는지 확인해야 해.
        password = request.data.get("password")
        # user를 만들 때, 만약 password가 없다면 ParseError를 발생시킴.
        if not password:
            raise ParseError
        serializer = PrivateUserSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            # 새로운 user를 받음
            user = serializer.save()
            # set_password에 user가 보낸 raw password를 넣어줌
            user.set_password(password)
            # hash 화된 password가 필요하기 때문에 user.save() 한번더 실행
            user.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PublicUser(APIView):

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        serializer = PublicUserSerializer(user)
        return Response(serializer.data)


# password 변경 (누군가 이 url로 호출하면, 그건 자기 자신의 password를 바꾸길 원하기 때문/ 다른 사람 걸 바꾸는게 아님)
# password를 바꾸는 과정은 user가 이전의 password를 주고, 새로운 password를 주면 그거로 바꾸는 거잖아. 이게 다야.
# django는 user의 password를 hash화해서 저장한다
class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        # 만약 old_password와 new_password 모두 해당되지 않으면, ParseError를 내보내자
        if not old_password or not new_password:
            raise ParseError
        # check_password는 True나 False를 반환하지
        # True or False를 반환 (기존의 password가 맞다면 user의 password를 업데이트할 거야)
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return ParseError


# authenticate function은 username과 password를 돌려주는 function인데, 만약 username과 password가 맞다면, django는 user를 리턴할거야.
class LogIn(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        # 이 함수(authenticate)는 user를 리턴할 수도 있고 아닐 수도 있어.
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        # 만약 user가 존재하면 user를 login하는 거야.
        # request 객체와 함께 login function을 호출하면 돼.
        # login function은 백엔드에서 user 정보가 담긴 session을 생성하고, 사용자에게 cookie를 보내줄거야.
        if user:
            login(request, user)
            return Response({"ok": "Welcome!"})
        else:
            return Response({"error": "Wrong password"})


class LogOut(APIView):
    # 이 class를 호출하기 위해선 로그인 되어 있어야 해
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "bye!"})


# JWT Encode(암호화)
class JWTLogIn(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        # 만약 username이나 password가 없으면 에러를 발생시킴
        if not username or not password:
            raise ParseError
        # 해당정보가 DB에 존재하면, user로 반환해주고, 아니면 false를 반환
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            # django 시크릿키를 이용한 토큰 암호화(서명)
            token = jwt.encode(
                {"pk": user.pk},
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            # 토큰 정보를 담은 Response를 유저에 반환
            return Response({"token": token})
        else:
            return Response({"error": "wrong password"})
