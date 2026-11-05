"""Модели данных Django ORM для сервиса учёта ошибок Freim."""

from django.db import models
from django.urls import reverse


class Severity(models.TextChoices):
    """Варианты уровней серьезности ошибки."""

    CRITICAL = "критическая", "Критическая"
    MAJOR = "значительная", "Значительная"
    MINOR = "незначительная", "Незначительная"


class Priority(models.TextChoices):
    """Варианты приоритетов устранения ошибки."""

    HIGH = "Высокий", "Высокий"
    MEDIUM = "Средний", "Средний"
    LOW = "Низкий", "Низкий"


class User(models.Model):
    """Пользователь, регистрирующий ошибки в системе."""

    name = models.CharField(
        max_length=200,
        verbose_name="Имя пользователя",
        help_text="Полное имя или логин пользователя",
    )
    email = models.EmailField(
        verbose_name="Электронная почта",
        help_text="Действующий адрес электронной почты",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.name} <{self.email}>"


class Developer(models.Model):
    """Разработчик, ответственный за исправление ошибок."""

    name = models.CharField(
        max_length=200,
        verbose_name="Имя разработчика",
        help_text="ФИО разработчика программного обеспечения",
    )
    specialization = models.CharField(
        max_length=200,
        verbose_name="Специализация",
        help_text="Основная технологическая специализация (Backend, Frontend)",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Разработчик"
        verbose_name_plural = "Разработчики"

    def __str__(self):
        return f"{self.name} ({self.specialization})"


class Status(models.Model):
    """Статус жизненного цикла ошибки."""

    name = models.CharField(
        max_length=100,
        verbose_name="Наименование статуса",
        help_text="Этап обработки ошибки (Новая, В работе, Закрыта и т.д.)",
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    def __str__(self):
        return self.name


class ErrorQuerySet(models.QuerySet):
    """Пользовательский QuerySet с методами фильтрации ошибок."""

    def active(self):
        """Ошибки, которые не закрыты и не исправлены."""
        return self.exclude(
            status__name__in=["Закрыта", "Исправлена"]
        )

    def critical(self):
        """Ошибки с критической серьезностью."""
        return self.filter(severity=Severity.CRITICAL)

    def high_priority(self):
        """Ошибки с высоким приоритетом."""
        return self.filter(priority=Priority.HIGH)

    def by_status(self, status_name):
        """Фильтрация ошибок по наименованию статуса."""
        return self.filter(status__name=status_name)


class ErrorManager(models.Manager.from_queryset(ErrorQuerySet)):
    """Пользовательский менеджер модели Error."""

    pass


class Error(models.Model):
    """Ошибка (дефект) программного продукта."""

    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок",
        help_text="Краткое описание обнаруженной ошибки",
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Подробное описание шагов воспроизведения и симптомов",
    )
    severity = models.CharField(
        max_length=50,
        choices=Severity.choices,
        default=Severity.MINOR,
        verbose_name="Серьезность",
        help_text="Уровень серьезности дефекта",
    )
    priority = models.CharField(
        max_length=50,
        choices=Priority.choices,
        default=Priority.LOW,
        verbose_name="Приоритет",
        help_text="Приоритет устранения дефекта",
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name="errors",
        verbose_name="Статус",
        help_text="Текущий статус жизненного цикла ошибки",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="errors",
        verbose_name="Пользователь",
        help_text="Пользователь, создавший отчёт об ошибке",
    )
    developer = models.ForeignKey(
        Developer,
        on_delete=models.PROTECT,
        related_name="errors",
        verbose_name="Разработчик",
        help_text="Разработчик, назначенный на устранение ошибки",
    )

    objects = ErrorManager()

    class Meta:
        ordering = ["id"]
        verbose_name = "Ошибка"
        verbose_name_plural = "Ошибки"

    def __str__(self):
        return f"#{self.id} {self.title}"

    def get_absolute_url(self):
        return reverse(
            "bugtracker:error_detail",
            kwargs={"error_id": self.id},
        )

    def close(self):
        """Переводит ошибку в статус 'Закрыта'."""
        closed_status = Status.objects.filter(name="Закрыта").first()
        if closed_status:
            self.status = closed_status
            self.save(update_fields=["status"])
