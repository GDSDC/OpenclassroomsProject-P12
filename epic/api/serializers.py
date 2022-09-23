from django.contrib.auth import authenticate
from rest_framework import serializers

from core.contacts.models import Contact
from core.users.models import User


class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * email
      * password.
    It will try to authenticate the user with when validated.
    """
    email = serializers.CharField(
        label="Email",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take email and password from request
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong email or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "email" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs


class SignUpSerializer(serializers.ModelSerializer):
    """Serializer for signup new user"""
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'phone', 'mobile', 'role']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'role': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', ''),
            mobile=validated_data.get('mobile', ''),
            role=validated_data.get('role'),
        )

        user.set_password(validated_data['password1'])
        user.save()

        return user


class ContactSerializer(serializers.ModelSerializer):
    """Serializer for Contact (client or prospect)."""

    class Meta:
        model = Contact
        fields = ['sales', 'first_name', 'last_name', 'phone', 'mobile', 'company_name', 'is_client']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'phone': {'required': True},
            'company_name': {'required': True},
        }

    def create(self, validated_data):
        contact = Contact.objects.create(
            sales=User.objects.get(id=int(validated_data.get('sales')))
            if validated_data.get('sales', None) is not None else None,
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            phone=validated_data.get('phone'),
            mobile=validated_data.get('mobile', ''),
            company_name=validated_data.get('company_name'),
            is_client=validated_data.get('is_client', False),
        )
        contact.save()

        return contact
