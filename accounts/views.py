from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from django.shortcuts import render
from django.contrib.auth import logout as django_logout
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
from rest_framework import status, permissions, views
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import permission_classes
from rest_framework.generics import UpdateAPIView, get_object_or_404, ListAPIView
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.models import User, Profile, Interest, UserManager
from accounts.permission import IsOwnerOrReadOnly
from accounts.serializers import (
    CustomTokenObtainPairSerializer,
    GetFullUserSerializer,
    UpdateProfileSerializer,
    UserSerializerWithToken,
    ProfileSerializer,
    GetFullProfileSerializer,
    InterestSerializer,
)
from . import constants


def initialize_backend():
    try:
        # Populate
        if Interest.objects.count() == 0:
            Interest.objects.bulk_create(
                [Interest(**one) for one in constants.INTERESTS], ignore_conflicts=True
            )
            print("[INITIALIZATION][SUCCESS]: INTERESTS populated")
        else:
            print("[INITIALIZATION][EXISTS]: INTERESTS already populated")
    except Exception as e:
        print("[INITIALIZATION][ERROR]:", str(e))
    try:
        # Populate
        superuser = User.objects.create_superuser(
            email="admin@admin.com", username="admin", password="admin"
        )
        print("[INITIALIZATION][SUCCESS]: SUPER ADMIN added")
    except Exception as e:
        print("[INITIALIZATION][ERROR]:", str(e))


# Call the function to initialize the backend
# initialize_backend()


class GoogleAuthView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

    def get_response(self):
        response = super().get_response()
        print(response)
        if "access_token" in response.data:
            refresh = RefreshToken.for_user(response.user)
            response.data["refresh"] = str(refresh)
            response.data["access"] = str(refresh.access_token)
        return response


class GoogleAuthLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        if email:
            user = User.objects.filter(email=email, isGoogle=True)
            exists = user.exists()
            if exists:
                user = user.first()
                serializer = GetFullUserSerializer(user)
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "user": serializer.data,
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                    status=status.HTTP_200_OK,
                )
            return Response({"manual": True}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Please provide an email address."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RegisterView(APIView):
    # authentication_classes = [AllowAny]
    permission_classes = [AllowAny]
    serializer_class = UserSerializerWithToken

    @swagger_auto_schema(
        request_body=UserSerializerWithToken,
        # responses={
        #     201: 'User registration successful',
        #     400: 'Bad request',
        # }
    )
    def post(self, request, *args, **kwargs):
        error_result = {}

        serializer = UserSerializerWithToken(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            print(access_token)

            output = "Successfully accounts created."
            content = {"status": True, "message": output}
            return Response(content, status=status.HTTP_200_OK)
        content = {
            "status": False,
            "message": serializer.errors,
            "result": error_result,
        }
        return Response(content, status=status.HTTP_200_OK)


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
        except AuthenticationFailed as e:
            # Handle the authentication failed exception
            error_message = "Invalid email or password."
            return self.custom_error_response(error_message)

        return self.process_response(response)

    def process_response(self, response):
        res = response.data

        if response.status_code == 200 and "access" in res:
            email = self.request.data.get("email")
            user = User.objects.filter(email=email).first()

            if user:
                if not user.check_password(self.request.data.get("password")):
                    error_message = "Invalid email or password."
                    return self.custom_error_response(error_message)

                serializer = GetFullUserSerializer(
                    user, context={"request": self.request}
                )
                res["user"] = serializer.data
            else:
                error_message = "Invalid email or password."
                return self.custom_error_response(error_message)

        return Response(res)

    def custom_error_response(self, error_message):
        return Response(
            {"status": False, "message": error_message, "result": {}},
            status=status.HTTP_200_OK,
        )


class CheckEmailExistsView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        if email:
            user_exists = User.objects.filter(email=email).exists()
            return Response({"email_exists": user_exists}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Please provide an email address."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PublicUserProfile(APIView):
    permission_classes = [AllowAny]

    def get(self, request, username_slug, *args, **kwargs):
        user = get_object_or_404(User, username_slug=username_slug)
        if user:
            serializer = GetFullUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class ImportList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        id = request.data.get("id")
        if id:
            profile = get_object_or_404(Profile, user__id=int(id))
            if profile:
                profile.list_import_count += 1
                profile.save()
                return Response({}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        django_logout(request)
        return Response(status=204)


class ProfileUpdateAPIView(UpdateAPIView):
    # authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    # permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "user_id"
    serializer_class = UpdateProfileSerializer
    queryset = Profile.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        serializer_full = GetFullUserSerializer(instance.user)

        output = "Successfully updated account"
        response_data = {
            "status": True,
            "message": {"success": [output]},
            "result": serializer_full.data,
        }
        return Response(response_data)


@permission_classes([AllowAny])
class InterestListView(ListAPIView):
    pagination_class = LimitOffsetPagination
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
