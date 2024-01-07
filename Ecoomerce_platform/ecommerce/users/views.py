from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer
from django.contrib.auth.models import User
from rest_framework import generics
from django.contrib.auth import authenticate,logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from rest_framework import  status,serializers
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            user = serializer.data
            return Response(
                {"message": "User registered successfully","data":user},
                status=status.HTTP_201_CREATED,
            )
        except serializers.ValidationError as e:
            # Include validation error messages in the response
            return Response({"error_messages": e.detail,"data": serializer.data,}, status=status.HTTP_400_BAD_REQUEST)
        


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not (email and password):
            return Response({"message": "Please provide both email and password."},status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)

        if user is not None:
            try:
                user_info = {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                }
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Login successful',
                    'user_info':user_info,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),

                   
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": f"Token creation error: {str(e)}"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Invalid email or password."},status=status.HTTP_401_UNAUTHORIZED)
@method_decorator(csrf_exempt, name='dispatch')       
class LogoutView(APIView):
    def post(self, request):
        print(request)
        try:
            refresh_token = request.data.get("refresh")
            print(refresh_token)
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"message": "Logout successful"},status=status.HTTP_200_OK)
            else:
                return Response({"message": "Refresh token not provided"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"message": f"Error during logout: {str(e)}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)