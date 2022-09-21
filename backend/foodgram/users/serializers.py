from users.models import User
from djoser.serializers import UserSerializer
from rest_framework import serializers


class CustomUserSerializer(UserSerializer):
    """Сериализатор кастомной модели пользователя."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous or (user == obj):
            return False
        return user.following.filter(id=obj.id).exists()

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['lastname'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
