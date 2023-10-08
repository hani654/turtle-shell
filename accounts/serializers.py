from rest_framework import serializers
from accounts.models import User
from django.contrib.auth import get_user_model


class UserInfoSerializer(serializers.ModelSerializer):
    styles = serializers.SerializerMethodField()

    def get_styles(self, obj):
        queryset = obj.styles.all()
        return [{"id": style.id, "name": style.name} for style in queryset]

    class Meta:
        model = get_user_model()
        fields = ("email", "nickname", "image", "styles")


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
            "password",
            "nickname",
        )
        extra_kwargs = {"password": {"write_only": True}}

    normalized_fields = ["username", "email", "nickname"]

    def is_valid(self, *, raise_exception=False):
        for field in self.normalized_fields:
            if field == "email":
                self.initial_data["email"] = get_user_model().objects.normalize_email(
                    self.initial_data.get(field)
                )
            else:
                self.initial_data[field] = (
                    get_user_model()
                    .normalize_username(self.initial_data.get(field) or "")
                    .lower()
                )
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password")
        user = super().update(instance, validated_data)
        user.set_password(password)
        user.save()
        return user


class FollowListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    nickname = serializers.CharField()

    followers = serializers.SerializerMethodField()
    followees = serializers.SerializerMethodField()

    def get_followers(self, obj):
        queryset = obj.followers.all()
        return [
            {"id": follower.id, "nickname": follower.nickname} for follower in queryset
        ]

    def get_followees(self, obj):
        queryset = obj.followees.all()
        return [
            {"id": followee.id, "nickname": followee.nickname} for followee in queryset
        ]

    class Meta:
        model = get_user_model()
        fields = ("id", "nickname", "followers", "followees")