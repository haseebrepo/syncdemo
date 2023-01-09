from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from .serializers import CustomUserSerializer, CustomUserLoginSerializer
from .models import User

# Create your views here.
status_200_ok = status.HTTP_200_OK
status_created_201 = status.HTTP_201_CREATED
status_bad_req_400 = status.HTTP_400_BAD_REQUEST
status_un_auth_401 = status.HTTP_401_UNAUTHORIZED

class CustomUserCreateView(APIView):

    def post(self, request, *args, **kwargs):
        
        data = request.data
        if not data:
            return Response({'data':[], 'success':False, 'message':'Please Enter Data To Register User'}, status_bad_req_400)
        else:
            if User.objects.filter(email=data.get('email')).first():
                return Response({'data':[], 'success':False, 'message': 'User with this email already exist'},status_bad_req_400)
        
        # data['username'] = data.get('email')
        try:
            data['is_active'] = True
            serializer = CustomUserSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response_data = serializer.data
                tokens = {'access': str(AccessToken.for_user(serializer.instance)),'refresh': str(RefreshToken.for_user(serializer.instance).access_token)}
                response_data['tokens'] = tokens
                status_code = status_created_201
                response = {'data': response_data, 'success': True, 'message':'Vendor has been Registered Successfully', 'status_code': status_code}
                return Response(response, status_code)
            return Response({'data':[], 'success':False, 'message':serializer.errors, 'status_code':status_bad_req_400}, status=status_bad_req_400)
        except Exception as e:
            return Response({'data':[], 'success':False, 'message':str(e), 'status_code':status_bad_req_400}, status=status_bad_req_400)



class UserLoginView(APIView):

    def post(self, request, *args, **kwargs):

        try:
            data = User.objects.filter(email=request.data.get('email')).first()
            if not data:
                status_code = status_bad_req_400
                return Response({'data':[], 'success':False, 'message':'User does not exist', 'status_code':status_code}, status=status_bad_req_400)
            if not data.check_password(request.data.get('password')):
                status_code = status_bad_req_400
                return Response({'data':[], 'success':False, 'message':'You have entered an incorrect password', 'status_code':status_code}, status=status_bad_req_400)

            if data:
                serializer = CustomUserLoginSerializer(data, many=False)
                if serializer:
                    response_data = serializer.data
                    response_data['tokens'] = {'access': str(AccessToken.for_user(serializer.instance)),'refresh': str(RefreshToken.for_user(serializer.instance).access_token)}
                    status_code = status_200_ok
                    response = {'data': response_data, 'success':True, 'message':f"""Hey! {response_data.get('full_name')} You are logged in successfully""", 'status_code':status_code}
 
        except Exception as e:
            status_code = status_bad_req_400
            response = {'data':[], 'success':False, 'message':str(e), 'status_code':status_code}
        return Response(response, status_code)