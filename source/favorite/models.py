from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


class Favorite(models.Model):
    session_key = models.CharField(
        max_length=40, null=True, blank=True, verbose_name="Ключ сессии"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Пользователь",
    )
    part = models.ForeignKey(
        "part.Part",
        related_name="favorites",
        on_delete=models.CASCADE,
        verbose_name="Запчасть",
    )

    def __str__(self):
        return f"Избранное: {self.part}"

    def clean(self):
        if not self.user and not self.session_key:
            raise ValidationError(
                "Необходимо указать либо пользователя, либо ключ сессии."
            )
        if self.user and self.session_key:
            raise ValidationError(
                "Нельзя указывать одновременно пользователя и ключ сессии."
            )

    def to_display(self):
        return [self.user, self.part]

    def get_column_headers(self):
        return ['Пользователь', "Товар"]

    class Meta:
        db_table = "favorite"
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "part"], name="unique_user_favorite"
            ),
            models.UniqueConstraint(
                fields=["session_key", "part"], name="unique_session_favorite"
            ),
        ]
        indexes = [
            models.Index(fields=["session_key"]),
            models.Index(fields=["user"]),
        ]
