from rest_framework import serializers
from todo.models import Task
from django.contrib.auth.models import User


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = [
            "id",
            "user",
            "title",
            "complete",
            "created_date",
            "updated_date",
        ]
        read_only_fields = ["user"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["user"] = UserSerializer(instance.user).data
        return rep


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username"]
