from rest_framework.response import Response
from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    EmptySerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainSerializer,
    ChangePasswordSerializer,
)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework import status, generics
from rest_framework import viewsets
from rest_framework.views import APIView
from django.core.exceptions import ImproperlyConfigured
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [
        AllowAny,
    ]
    serializer_class = EmptySerializer
    serializer_classes = {
        "login": LoginSerializer,
        "register": RegisterSerializer,
    }

    @action(
        methods=[
            "POST",
        ],
        detail=False,
    )
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get("user")
            if user is not None and user.is_active:
                login(request, user)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=[
            "POST",
        ],
        detail=False,
    )
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password1"]
            user = User.objects.create_user(username=username, password=password)
            authenticate(request, username=username, password=password)
            login(request, user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def logout(self, request):
        logout(request)
        data = {"success": "Sucessfully logged out"}
        return Response(data=data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()


class CustomObtaionAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "username": user.username,
            }
        )


class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response("Token has been deleted.", status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer


class ChangePasswordView(generics.GenericAPIView):
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": "wrong password"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"detail": "Password has been changed successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LogoutViewSet(viewsets.ViewSet):
#     def retrieve(self,request, pk=None):
#         logout(request)
#         return Response(
#             {"non_field_errors": "successfully logged out"},
#             status=status.HTTP_200_OK,
#         )


# class RegisterViewSet(viewsets.ViewSet):
#     serializer_class = RegisterSerializer

#     def create(self, request):
#         serializer = RegisterSerializer(data=request.data, many=False)
#         if serializer.is_valid():
#             username = serializer.validated_data['username']
#             password = serializer.validated_data['password1']
#             user = User.objects.create_user(
#                 username=username, password=password
#             )
#             authenticate(request, username=username, password=password)
#             login(request, user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

# class LoginViewSet(viewsets.ViewSet):
#     serializer_class = LoginSerializer


#     def create(self, request, *args, **kwargs):
#         serializer = LoginSerializer(data=request.data, many=False)
#         if serializer.is_valid():
#             user = serializer.validated_data.get('user')
#             if user is not None and user.is_active:
#                 login(request, user)
#                 return Response(serializer.data , status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
