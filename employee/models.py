from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.templatetags.static import static


class AuditedModel(models.Model):
    created_at = models.DateTimeField("дата добавления", auto_now_add=True)
    modified_at = models.DateTimeField("дата изменения", auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, AuditedModel):
    class Meta:
        db_table = "users"
        verbose_name = "сотрудник"
        verbose_name_plural = "сотрудники"

    def __str__(self):
        return self.email if self.email else self.username

    @property
    def avatar_url(self):
        return static("formula/images/avatar.jpg")

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.last_name}, {self.first_name}"

        return None


class Profile(AuditedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField("аватар", null=True, blank=True, default=None)
    resume = models.FileField("резюме", null=True, blank=True, default=None)
    link = models.URLField("ссылка", null=True, blank=True)
    data = models.JSONField("данные", null=True, blank=True)

    class Meta:
        db_table = "profiles"
        verbose_name = "профиль"
        verbose_name_plural = "профили"
