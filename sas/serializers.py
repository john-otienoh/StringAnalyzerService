from rest_framework import serializers
from django.utils import timezone
from .models import StringRecord
from .helpers import *
import hashlib


class StringCreateSerializer(serializers.ModelSerializer):
    value = serializers.CharField(required=True)

    class Meta:
        model = StringRecord
        fields = ["value"]

    def validate_value(self, value):
        if not value:
            raise serializers.ValidationError("Missing 'value' field.")

        if not isinstance(value, str):
            raise serializers.ValidationError("Value must be a string.")

        if StringRecord.objects.filter(value=value).exists():
            raise serializers.ValidationError("String already exists in the system.")

        return value

    def create(self, validated_data):
        value = validated_data["value"]

        length = len(value)
        is_palindrome = is_palindrome(value)
        unique_characters = count_unique_characters(value)
        word_count = compute_word_count(value)
        sha_hash = compute_sha256(value)

        # Character frequency map
        freq_map = character_frequency_map(value)

        # --- Create record ---
        record = StringRecord.objects.create(
            id=sha_hash,
            value=value,
            length=length,
            is_palindrome=is_palindrome,
            unique_characters=unique_characters,
            word_count=word_count,
            character_frequency_map=freq_map,
            created_at=timezone.now(),
        )
        return record

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "value": instance.value,
            "properties": {
                "length": instance.length,
                "is_palindrome": instance.is_palindrome,
                "unique_characters": instance.unique_characters,
                "word_count": instance.word_count,
                "sha256_hash": instance.id,
                "character_frequency_map": instance.character_frequency_map,
            },
            "created_at": instance.created_at.isoformat(),
        }


class StringRecordSerializer(serializers.ModelSerializer):
    """Used for GET responses"""

    class Meta:
        model = StringRecord
        fields = [
            "id",
            "value",
            "length",
            "is_palindrome",
            "unique_characters",
            "word_count",
            "character_frequency_map",
            "created_at",
        ]

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "value": instance.value,
            "properties": {
                "length": instance.length,
                "is_palindrome": instance.is_palindrome,
                "unique_characters": instance.unique_characters,
                "word_count": instance.word_count,
                "sha256_hash": instance.id,
                "character_frequency_map": instance.character_frequency_map,
            },
            "created_at": instance.created_at.isoformat(),
        }

