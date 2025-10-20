from django.db import models
from django.utils import timezone

class StringRecord(models.Model):
    """
    Represents an analyzed string and its computed properties.
    """
    id = models.CharField(
        max_length=64,
        primary_key=True,
        editable=False,
        help_text="SHA-256 hash of the string (unique identifier)"
    )
    value = models.TextField(
        unique=True,
        help_text="Original string value provided by user"
    )
    length = models.PositiveIntegerField(
        help_text="Number of characters in the string"
    )
    is_palindrome = models.BooleanField(
        help_text="Whether the string reads the same forwards and backwards"
    )
    unique_characters = models.PositiveIntegerField(
        help_text="Count of distinct characters"
    )
    word_count = models.PositiveIntegerField(
        help_text="Number of words in the string"
    )
    character_frequency_map = models.JSONField(
        help_text="Dictionary mapping each character to its frequency"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
        help_text="Timestamp of when the string was analyzed and stored"
    )

    class Meta:
        db_table = "stringrecords"
        ordering = ["-created_at"]
        verbose_name = "String Record"
        verbose_name_plural = "String Records"

    def __str__(self):
        return f"{self.value[:30]}... ({self.id})"

