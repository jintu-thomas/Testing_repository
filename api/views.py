   from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserRegister,UpdateSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


# Create your views here.


class register(APIView):
    def post(self,request,format=None):
        data={}
        serializer=UserRegister(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            # data['response']='registered'
            data['username']=account.username
            data['email']=account.email
            token,create = Token.objects.get_or_create(user=account)
            data['token']=token.key

        else:
            data= serializer.errors
        return Response(data)
#---------------------------------------------------------------------------------------------------------------------------------------  
#--------------------------------------------------------------------------------------------------------------------------------------
class welcome(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        content = {"user":str(request.user),"userid":str(request.user.id)}
        return Response(content)



#--------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------


from django.contrib.auth.models import User

class Update(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self,request,user_id):
        res={}
        user = User.objects.get(pk=user_id)
        if user:
            serializer=UpdateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save_fields(user)
                res['response']='success'
        else:
            res['response']='fail'
        return Response(res)
#----------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------

class logout(APIView):

    def get(self,request,format=None):
        data={}
        request.user.auth_token.delete()
        
        data['status'] = 'succcess'
        data['message']='successfully logout'
        data['status_code']=200
        return Response(data)
#--------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------



from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

