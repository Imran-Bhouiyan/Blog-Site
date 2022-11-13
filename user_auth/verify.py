import jwt
from rest_framework.authentication import BaseAuthentication
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
from . models import User , TokenRecord
from django.conf import settings
from django.http.response import JsonResponse
from rest_framework import status


class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request , reason = None):
        return reason



class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return None
        try:
            access_token = authorization_header.split(' ')[1]
            payload = jwt.decode( 
                access_token , settings.HASHKEY , algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access token expired')
        except IndexError:
            raise exceptions.AuthenticationFailed("Token prefix missing")
        try:
            blacklist_query = TokenRecord.objects.filter(token = access_token).last()
        except:
            blacklist_query = None 
        if not blacklist_query:
            user = User.objects.filter(user_id = payload["user_id"]).first()

            if user is None:
                raise exceptions.AuthenticationFailed("User Not Found")
            if not user.is_active:
                raise exceptions.AuthenticationFailed("User is deactive")
            # if not user.is_verified:
            #     raise exceptions.AuthenticationFailed("User is not verified yet!")
            

            # self.enforce_csrf(request)
            return (user , None)
        else:
            raise exceptions.AuthenticationFailed("You are logout please login again.")

def enforce_csrf(self,request):
   
    check = CSRFCheck()
    check.process_request(request)
    reason = check.process_view(request , None , () , {})
    if reason:
        raise exceptions.PermissionDenied('CSRF Failed : %s' % reason )