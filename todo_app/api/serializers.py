from rest_framework import serializers
from todo_app.models import Todo, User

class TodoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField()
    completed = serializers.BooleanField()
    to_be_completed = serializers.DateField()
    created_at = serializers.DateField(read_only=True)
    updated_at = serializers.DateField(read_only=True)

    def create(self, validated_data):
        return Todo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.completed = validated_data.get('completed', instance.completed)
        instance.to_be_completed = validated_data.get('to_be_completed', instance.to_be_completed)
        instance.save()

        return (instance)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        read_only_fields = ('id')
