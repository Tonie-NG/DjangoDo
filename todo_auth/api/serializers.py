from rest_framework import serializers
from todo_auth.models import User

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()
    created_at = serializers.DateField(read_only=True)
    updated_at = serializers.DateField(read_only=True)

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.save()

        return (instance)
