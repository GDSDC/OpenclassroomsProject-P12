from django.contrib.auth import authenticate
from rest_framework import serializers

from core.contacts.models import Contact
from core.contracts.models import Contract
from core.events.models import Event
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
            sales=User.objects.get(id=int(validated_data.get('sales').id))
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

    def update(self, instance, validated_data):
        instance.sales = User.objects.get(id=int(validated_data.get('sales', instance.sales).id)) \
            if validated_data.get('sales', instance.sales) is not None else None
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.is_client = validated_data.get('is_client', instance.is_client)
        instance.save()
        return instance


class ContractSerializer(serializers.ModelSerializer):
    """Serializer for Contract."""

    class Meta:
        model = Contract
        fields = ['client', 'sales', 'status', 'amount', 'payment_due']
        extra_kwargs = {
            'client': {'required': True}
        }

    def create(self, validated_data):
        contract = Contract.objects.create(
            client=Contact.objects.get(id=self.context.get('contact_id')),
            sales=User.objects.get(id=int(validated_data.get('sales').id))
            if validated_data.get('sales', None) is not None else None,
            status=validated_data.get('status', False),
            amount=validated_data.get('amount', 0),
            payment_due=validated_data.get('payment_due', ''),
        )
        contract.save()
        return contract

    def update(self, instance, validated_data):
        instance.sales = User.objects.get(id=int(validated_data.get('sales', instance.sales).id)) \
            if validated_data.get('sales', instance.sales) is not None else None
        instance.status = validated_data.get('status', instance.status)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.payment_due = validated_data.get('payment_due', instance.payment_due)
        instance.save()
        return instance


class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event"""

    class Meta:
        model = Event
        fields = ['client', 'support', 'status', 'attendees', 'event_date', 'notes']
        extra_kwargs = {
            'client': {'required': True}
        }

    def create(self, validated_data):
        event = Event.objects.create(
            client=Contact.objects.get(id=self.context.get('contact_id')),
            support=User.objects.get(id=int(validated_data.get('support').id))
            if validated_data.get('support', None) is not None else None,
            status=validated_data.get('status', False),
            attendees=validated_data.get('attendees', ''),
            event_date=validated_data.get('event_date', ''),
            notes=validated_data.get('notes', ''),
        )
        event.save()
        return event

    def update(self, instance, validated_data):
        instance.support = User.objects.get(id=int(validated_data.get('support', instance.support).id)) \
            if validated_data.get('support', instance.support) is not None else None
        instance.status = validated_data.get('status', instance.status)
        instance.attendees = validated_data.get('attendees', instance.attendees)
        instance.event_date = validated_data.get('event_date', instance.event_date)
        instance.notes = validated_data.get('notes', instance.notes)
        instance.save()
        return instance
