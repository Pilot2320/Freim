"""Модели данных Django ORM для сервиса учёта ошибок Freim."""

from django.db import models
from django.urls import reverse


class User(models.Model):
    """Пользователь, регистрирующий ошибки в системе."""

    name = models.CharField(
        max_length=200,
        verbose_name="Имя пользователя",
    )
    email = models.EmailField(
        verbose_name="Электронная почта",
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
    )
    specialization = models.CharField(
        max_length=200,
        verbose_name="Специализация",
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
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    def __str__(self):
        return self.name


class Error(models.Model):
    """Ошибка (дефект) программного продукта."""

    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок",
    )
    description = models.TextField(
        verbose_name="Описание",
    )
    severity = models.CharField(
        max_length=50,
        verbose_name="Серьезность",
    )
    priority = models.CharField(
        max_length=50,
        verbose_name="Приоритет",
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name="errors",
        verbose_name="Статус",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="errors",
        verbose_name="Пользователь",
    )
    developer = models.ForeignKey(
        Developer,
        on_delete=models.PROTECT,
        related_name="errors",
        verbose_name="Разработчик",
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Ошибка"
        verbose_name_plural = "Ошибки"

    def __str__(self):
        return f"#{self.id} {self.title}"

    def get_absolute_url(self):
        return reverse("bugtracker:error_detail", kwargs={"error_id": self.id})
