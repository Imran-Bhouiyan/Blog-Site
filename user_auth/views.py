from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from .models import *
from .serializers import *
from django.contrib.auth.hashers import make_password
import jwt
from rest_framework import exceptions
from django.conf import settings
from rest_framework import permissions
import requests
import random
import datetime
import string
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.utils import timezone

from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.utils.html import strip_tags
from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend
import uuid
current_datetime = timezone.localtime(timezone.now())

current_date = timezone.now().date()


def genarate_access_token(user):
    access_token_payload = {
        "user_id": user.user_id,
        "exp": current_datetime + timezone.timedelta(days=0, minutes=60),
        "iat": current_datetime,
    }
    access_token = jwt.encode(access_token_payload, settings.HASHKEY, algorithm="HS256")
    return access_token


def genarate_refresh_token(user):
    refresh_token_payload = {
        "user_id": user.user_id,
        "exp": current_datetime + timezone.timedelta(days=7),
        "iat": current_datetime,
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.HASHKEY, algorithm="HS256"
    )
    return refresh_token

# In this API user can register 

@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    try:
        SpecialSym = "!@#$%^&*()-+?_=,<>/"
        password = request.data.get("password")
        email = request.data.get("email")

        if password == "" or email == "":
            return JsonResponse({"status": status.HTTP_406_NOT_ACCEPTABLE,  "msg": "Please check your data!"})
        else:
            if len(password) < 8 or len(password) > 20 :
                return JsonResponse({"status": status.HTTP_406_NOT_ACCEPTABLE , "msg":"Password must be gretter than 8 character and less than 20 character. " })
            if not any(char.isdigit() for char in password):
                return JsonResponse({"status": status.HTTP_406_NOT_ACCEPTABLE , "msg":"Password should have at least one numeral." })
            if not any(char.isupper() for char in password):
                return JsonResponse({"status": status.HTTP_406_NOT_ACCEPTABLE , "msg":"Password should have at least one uppercase letter." })
            if not any(char.islower() for char in password):
                return JsonResponse({"status": status.HTTP_406_NOT_ACCEPTABLE , "msg":"Password should have at least one lowercase letter" })
            if not any(char in SpecialSym for char in password):
                return JsonResponse({"status": status.HTTP_406_NOT_ACCEPTABLE , "msg":"Password should have at least one Special Character." })
            else:
                serializer = AuthUserSerializers(data=request.data)
                if serializer.is_valid():
                    password_hash = make_password(request.data.get("password"))
                    user_id = str(uuid.uuid4())
                    serializer.save(password=password_hash, user_id=user_id , is_active = True)
                    return JsonResponse(
                        {
                            "status": status.HTTP_201_CREATED,
                            "data": serializer.data,
                        }
                    )
                else:
                    return JsonResponse(
                        {
                            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                            "msg": serializer.errors,
                        }
                    )
    except Exception as e:
        return JsonResponse(
            {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "msg": e.args[0]}
        )

#This API is totally optional acording to your task list
@api_view(["POST"])
@permission_classes([AllowAny])
def send_verify_code(request):
    try:
        email = request.data["email"]
        user_info = User.objects.filter(email=email).last()
        if user_info:
            range_start = 10 ** (6 - 1)
            range_end = (10 ** 6) - 1
            verify_code = random.randint(range_start, range_end)
            create_OTP = VerifyCode.objects.create(
                user=user_info, phone=user_info.phone, code=verify_code, email=email
            )
            create_OTP.save()

            email_backend = EmailConfig.objects.filter().last()
            receiver_email = email
            email_port = email_backend.email_port
            email_host = email_backend.email_host
            sender_address = email_backend.email_host_user
            sender_pass = email_backend.email_host_password
            template = "send_verify_code.html"
            backend = EmailBackend(
                host=email_host,
                port=email_port,
                username=sender_address,
                password=sender_pass,
                use_tls=True,
                fail_silently=False,
            )
            template = render_to_string(
                template, {"name": user_info.username, "verification_code": verify_code}
            )
            text_content = strip_tags(template)
            email = EmailMultiAlternatives(
                subject="User Varification Code",
                body=text_content,
                from_email=sender_address,
                to=[receiver_email],
                connection=backend,
            )
            email.attach_alternative(template, "text/html")
            email.send()
            return JsonResponse(
                {
                    "status": status.HTTP_200_OK,
                    "msg": "Verifation code send to your email. ",
                }
            )
        else:
            return JsonResponse({"status":status.HTTP_404_NOT_FOUND })

    except Exception as e:
        return JsonResponse(
            {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "msg": e.args[0]}
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def verify_user(request):
    try:
        email = request.data["email"]
        code = request.data["verification_code"]
        user_query = User.objects.filter(email=email).last()
        verification_code_query = VerifyCode.objects.filter(email=email).last()
        if user_query:
            if user_query.email == email and int(code) == verification_code_query.code :
                user_query.is_verified = True
                user_query.save()
                verification_code_query.delete()
                return JsonResponse({"status":status.HTTP_200_OK , "msg":"user verify successfully"})
                
            else:
                return JsonResponse(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "msg": "verification code not matched!",
                    }
                )
        else:
            return JsonResponse(
                {"status": status.HTTP_404_NOT_FOUND, "msg": "User not Found!"}
            )
    except Exception as e:
        return JsonResponse(
            {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "msg": e.args[0]}
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    email = request.data["email"]
    password = request.data["password"]
    response = Response()
    if (email is None) or (password is None):
        raise exceptions.AuthenticationFailed("email and password are required")
    user_info = User.objects.filter(email=email).last()
    if user_info is None:
        raise exceptions.AuthenticationFailed("User not found")
    if not user_info.check_password(password):
        raise exceptions.AuthenticationFailed("Wrong Password")
    serializers_data = AuthUserSerializers(user_info)
    access_token = genarate_access_token(user_info)
    refresh_token = genarate_refresh_token(user_info)
    response.set_cookie(key="refreshtoken", value=refresh_token, httponly=True)
    return JsonResponse(
        {
            "status": status.HTTP_200_OK,
            "data": serializers_data.data,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    )



