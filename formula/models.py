from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from simple_history.models import HistoricalRecords

from formula.encoders import PrettyJSONEncoder


class ActivityCategory(models.TextChoices):
    STANDARD = "STANDARD", _("Стандартный")
    BEDRIDDEN = "BEDRIDDEN", _("Лежачий")


class AuditedModel(models.Model):
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    modified_at = models.DateTimeField(_("modified at"), auto_now=True)

    class Meta:
        abstract = True


class Room(AuditedModel):
    name = models.TextField(max_length=100)
    category = models.CharField(
        _("category"),
        choices=ActivityCategory,
        null=True,
        blank=False,
        max_length=255,
    )
    price_per_day = MoneyField(max_digits=8, decimal_places=2, default_currency="RUB")
    description = models.TextField(max_length=300)
    picture = models.ImageField(_("picture"), null=True, blank=True, default=None)
    history = HistoricalRecords()
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        db_table = "rooms"
        verbose_name = _("room")
        verbose_name_plural = _("rooms")

    def __str__(self):
        return self.name


class Client(AuditedModel):
    first_name = models.CharField(_("first name"), max_length=255)
    last_name = models.CharField(_("last name"), max_length=255)
    middle_name = models.CharField(_("last name"), max_length=255)
    category = models.CharField(
        _("category"),
        choices=ActivityCategory,
        null=True,
        blank=False,
        max_length=255,
    )
    phone = models.TextField(max_length=50)
    description = models.TextField(max_length=300)
    document = models.FileField(_("document"), null=True, blank=True, default=None)
    born_at = models.DateField(_("born"), null=True, blank=True)    
    history = HistoricalRecords()

    class Meta:
        db_table = "clients"
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"
        permissions = (("update_statistics", _("Update statistics")),)
        indexes = [
            models.Index(fields=["category"]),
        ]


    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}, {self.middle_name}"

    @property
    def initials(self):
        return f"{self.last_name} {self.first_name[0]}.{self.middle_name[0]}."
    

class Booking(AuditedModel):
    room = models.ForeignKey(
        "Room",
        verbose_name=_("room"),
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
    )
    client = models.ForeignKey(
        "Client",
        verbose_name=_("client"),
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
    )
    responsible = models.ForeignKey(
        "User",
        verbose_name=_("responsible"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="booking_responsible",
    )

    class Meta:
        db_table = "bookings"
        verbose_name = _("booking")
        verbose_name_plural = _("bookings")


class BookingWithFilters(Booking):
    history = HistoricalRecords()

    class Meta:
        proxy = True


class User(AbstractUser, AuditedModel):
    biography = models.TextField(_("biography"), null=True, blank=True, default=None)

    class Meta:
        db_table = "users"
        verbose_name = _("user")
        verbose_name_plural = _("users")

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
    picture = models.ImageField(_("picture"), null=True, blank=True, default=None)
    resume = models.FileField(_("resume"), null=True, blank=True, default=None)
    link = models.URLField(_("link"), null=True, blank=True)
    data = models.JSONField(_("data"), null=True, blank=True)

    class Meta:
        db_table = "profiles"
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")
