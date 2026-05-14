from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User
from .serializers import SendVerifyCodeSerializer, VerifyCodeSerializer, UserInfoSerailzier

class SendVerificationCodeApiView(CreateAPIView):

    serializer_class = SendVerifyCodeSerializer

class LoginWithOtpApiView(GenericAPIView):
    serializer_class = VerifyCodeSerializer

    def post(self, request):
        serailzier = self.serializer_class(data = request.data)

        if serailzier.is_valid():
            user = User.objects.get(phone = serailzier.validated_data.get('phone'))
            user.is_verified = True
            user.save()

            refresh = RefreshToken.for_user(user=user)

            return Response({'access': str(refresh.access_token), 'refresh': str(refresh)})

        return Response({'details' : serailzier.errors})
    

class UserInfoApiView( RetrieveUpdateAPIView ):
    permission_classes = [IsAuthenticated]
    serializer_class = UserInfoSerailzier
    
    def get_object(self):
        return self.request.user


    
    



    
    


