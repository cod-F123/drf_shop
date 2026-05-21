from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User, AddressUser
from .serializers import SendVerifyCodeSerializer, VerifyCodeSerializer, UserInfoSerailzier, AddressUserSerializer
from .permissions import IsOwner

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

        return Response({'details' : serailzier.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class UserInfoApiView( RetrieveUpdateAPIView ):
    permission_classes = [IsAuthenticated]
    serializer_class = UserInfoSerailzier
    
    def get_object(self):
        return self.request.user


class UserAddressViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner,]
    serializer_class = AddressUserSerializer

    def get_queryset(self):
        return AddressUser.objects.filter(user = self.request.user)
    



    
    


