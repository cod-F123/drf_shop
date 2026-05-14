from rest_framework import serializers
from accounts.models import User, OtpCode, Profile


class SendVerifyCodeSerializer(serializers.ModelSerializer):
    otp_code = serializers.CharField(read_only=True)
    phone = serializers.CharField(max_length=13, min_length=11, write_only=True)

    def validate(self, attrs):

        user , created = User.objects.get_or_create(phone = attrs.get('phone'))

        if not created:
            last_otp = OtpCode.objects.filter(user = user).order_by('-created_at').first()

            if last_otp and not last_otp.is_expired:
                raise serializers.ValidationError({'error' : 'otp before sended'})
        
        attrs['user'] = user 
            

        return super().validate(attrs)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.pop('otp_code')

        rep['msg'] = 'code sended'

        return rep

    def create(self, validated_data):
        return OtpCode.objects.create(user = validated_data['user'])
    
    class Meta:
        model = OtpCode
        fields  = ['otp_code', 'phone']

class VerifyCodeSerializer(serializers.Serializer):
    otp_code = serializers.CharField()
    phone = serializers.CharField(max_length=13, min_length=11)

    def validate(self, attrs):

        otp_code = OtpCode.objects.filter(user__phone = attrs.get("phone")).order_by('-created_at').first()

        if not otp_code:
            raise serializers.ValidationError({'otp_code' : 'otp code not found'})
        
        if otp_code.is_expired or otp_code.can_try_times <= 0:
            raise serializers.ValidationError({'otp_code' : 'code expired'})

        if otp_code.otp_code != attrs.get('otp_code'):
            otp_code.can_try_times -= 1
            otp_code.save()
            raise serializers.ValidationError( {'otp_code' : 'invalid code'})

        return super().validate(attrs)

    class Meta:
        fields = ['otp_code', 'phone']
        writeonly_fields = ['otp_code', 'phone']

class UserInfoSerailzier(serializers.ModelSerializer):
    full_name = serializers.CharField(required = False)

    def update(self, instance, validated_data):

        if validated_data.get('full_name', None):
            user_profile = Profile.objects.get(user = self.context["request"].user)

            user_profile.full_name = validated_data.get('full_name',None)
            user_profile.save()

            validated_data.pop('full_name')

        

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep['full_name'] = self.context['request'].user.profile.full_name

        return rep

    class Meta:
        model = User 
        fields = ['email', 'full_name']
