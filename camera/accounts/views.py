from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework import status, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import UserSerializer, UserLoginSerializer, ChangePasswordSerializer, ProfileSerializer
from .models import User, Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import APIException, NotFound


# Create your views here.
class RegisterView(views.APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'message': 'success',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return JsonResponse({
            'success': False,
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                refresh = TokenObtainPairSerializer.get_token(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
                return JsonResponse(data, status=status.HTTP_200_OK)

            return JsonResponse({
                        'success': False,
                        'error': 'Email or password is incorrect!',
                    }, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({
                    'success': False,
                    'error': serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return JsonResponse({
                'success': True
            }, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return JsonResponse({
                'success': False,
                'error': 'Bad Token'
            }, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(views.APIView):
    serializer_class = ChangePasswordSerializer
    model = User
    object = None

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if serializer.data.get('new_password_1') != serializer.data.get('new_password_2'):
                return JsonResponse({
                    'success': False,
                    'message': 'New password are not the same'
                }, status=status.HTTP_204_NO_CONTENT)
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return JsonResponse({
                    'success': False,
                    'error': 'Wrong old password.'
                }, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the email will get
            self.object.set_password(serializer.data.get("new_password_1"))
            self.object.save()

            return JsonResponse({
                'success': True,
                'message': 'Password updated successfully'
            }, status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({
            'success': False,
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    model = User
    object = None


class DeleteUserView(views.APIView):
    permission_classes = []
    model = User

    def get_object(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise NotFound(detail={
                'success': False,
                'detail': 'Not Found'
            }, code=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, *args, **kwargs):
        try:
            user = self.get_object(pk=pk)
            user.delete()
            return JsonResponse({
                'success': True
            }, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(views.APIView):
    permission_classes = []
    model = Profile
    serializer_class = ProfileSerializer

    def get_object(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise NotFound(detail={
                'success': False,
                'detail': 'Not Found'
            }, code=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, *args, **kwargs):
        user = self.get_object(pk)
        serializer = self.serializer_class(user)
        return JsonResponse({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, pk, *args, **kwargs):
        profile = self.get_object(pk)
        serializer = self.serializer_class(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'success': True, 'data': serializer.data}, status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({'success': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        profile = self.get_object(pk)
        profile.delete()
        return JsonResponse({
            'success': True
        }, status=status.HTTP_204_NO_CONTENT)
