from rest_framework import serializers
from .models import User



class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


    def validate_email(self,value):
        lower_email = value.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            serializers.ValidationError('Email Already Exists')
        
        return lower_email

    class Meta:
        model = User
        fields = '__all__'
    

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password:
            instance.set_password(password)
        
        instance.save()
        return instance


class CustomUserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = '__all__'