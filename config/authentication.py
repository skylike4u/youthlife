import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User


# JWT Decode(복호화)
class JWTAuthentication(BaseAuthentication):

    # authenticate 메소드 확장
    def authenticate(self, request):
        # print(request.headers)
        token = request.headers.get("Jwt")
        # 토큰이 없다면 None을 반환
        if not token:
            return None
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        # print(decoded)
        pk = decoded.get("pk")
        if not pk:
            raise AuthenticationFailed("Invalid Token")
        try:
            user = User.objects.get(pk=pk)
            # 튜플로 형태로 반환하는 게 rule이야. 이상하지만 따라야해
            return (user, None)
        except User.DoesNotExist:
            raise AuthenticationFailed("User Not Found")
