from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from simple_history.models import HistoricalRecords


class ActivityCategory(models.TextChoices):
    STANDARD = "STANDARD", "Стандартный"
    BEDRIDDEN = "BEDRIDDEN", "Лежачий"


class BookingStatus(models.TextChoices):
    NEW = "NEW", "Новая"
    PROGRESS = "PROGRESS", "В обработке"
    DONE = "DONE", "Обработана"


class AuditedModel(models.Model):
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    modified_at = models.DateTimeField("Дата изменения", auto_now=True)

    class Meta:
        abstract = True


class Room(AuditedModel):
    name = models.TextField(max_length=100)
    category = models.CharField(
        "Категория",
        choices=ActivityCategory,
        null=True,
        blank=False,
        max_length=255,
    )
    price_per_day = MoneyField("Цена за день", max_digits=8, decimal_places=2, default_currency="RUB")
    description = models.TextField("Описание", max_length=300)
    picture = models.ImageField("Фото", null=True, blank=True, default=None)
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    history = HistoricalRecords()

    class Meta:
        db_table = "rooms"
        verbose_name = "комната"
        verbose_name_plural = "комнаты"

    def __str__(self):
        return self.name


class Booking(AuditedModel):
    first_name = models.CharField("Имя", max_length=255)
    last_name = models.CharField("Фамилия", max_length=255)
    middle_name = models.CharField("Отчество", max_length=255, null=True, blank=True, default=None)
    age = models.IntegerField("Возраст")    
    description = models.TextField("Описание", max_length=300, null=True, blank=True, default=None)

    phone = models.TextField("Телефон", max_length=50)
    preferred_call_time = models.DateTimeField("Удобное время звонка", null=True, blank=True, default=None)
    preferred_check_in = models.DateTimeField("Дата и время заселения", null=True, blank=True, default=None)    

    preferred_budget = MoneyField("Бюджет/сутки", max_digits=8, decimal_places=2, default_currency="RUB", default=None, null=True, blank=True)
    room = models.ForeignKey(
        "Room",
        verbose_name="Комната",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
    )

    status = models.CharField(
        "Статус",
        choices=BookingStatus,
        null=False,
        blank=False,
        default=BookingStatus.NEW,
        max_length=30,
    )

    history = HistoricalRecords()

    class Meta:
        db_table = "bookings"
        verbose_name = "бронирование"
        verbose_name_plural = "бронирования"
        indexes = [
            models.Index(fields=["room", "status"]),
        ]

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}, {self.middle_name}"

    @property
    def initials(self):
        return f"{self.last_name} {self.first_name[0]}.{self.middle_name[0]}."
    