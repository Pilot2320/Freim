"""Настройка панели администратора Django для приложения bugtracker (ПР10)."""

from django.contrib import admin, messages
from django.db.models import Count

from .models import Developer, Error, Priority, Status, User


class ErrorInline(admin.TabularInline):
    """Встроенная таблица ошибок в карточке разработчика или пользователя."""

    model = Error
    fields = ("title", "severity", "priority", "status")
    extra = 0
    show_change_link = True


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    """Панель управления разработчиками."""

    list_display = ("id", "name", "specialization", "errors_count")
    list_display_links = ("id", "name")
    search_fields = ("name", "specialization")
    list_filter = ("specialization",)
    ordering = ("name",)
    inlines = (ErrorInline,)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_errors_count=Count("errors"))

    @admin.display(description="Количество ошибок", ordering="_errors_count")
    def errors_count(self, obj):
        return getattr(obj, "_errors_count", obj.errors.count())


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Панель управления пользователями."""

    list_display = ("id", "name", "email", "errors_count")
    list_display_links = ("id", "name")
    search_fields = ("name", "email")
    ordering = ("name",)
    inlines = (ErrorInline,)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_errors_count=Count("errors"))

    @admin.display(description="Количество ошибок", ordering="_errors_count")
    def errors_count(self, obj):
        return getattr(obj, "_errors_count", obj.errors.count())


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    """Панель управления статусами ошибок."""

    list_display = ("id", "name", "errors_count")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    ordering = ("id",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_errors_count=Count("errors"))

    @admin.display(description="Количество ошибок", ordering="_errors_count")
    def errors_count(self, obj):
        return getattr(obj, "_errors_count", obj.errors.count())


@admin.register(Error)
class ErrorAdmin(admin.ModelAdmin):
    """Панель управления дефектами (ошибками)."""

    list_display = (
        "id",
        "title",
        "severity",
        "priority",
        "status",
        "developer",
        "user",
    )
    list_display_links = ("id", "title")
    search_fields = (
        "title",
        "description",
        "developer__name",
        "user__name",
    )
    list_filter = ("severity", "priority", "status", "developer")
    ordering = ("id",)
    list_per_page = 10
    list_editable = ("priority",)
    readonly_fields = ("id",)
    autocomplete_fields = ("developer", "user", "status")
    save_on_top = True

    @admin.action(description="Установить статус 'Закрыта'")
    def mark_closed(self, request, queryset):
        closed_status = Status.objects.filter(name="Закрыта").first()
        if closed_status:
            updated = queryset.update(status=closed_status)
            self.message_user(
                request,
                f"Обновлено ошибок: {updated}.",
                messages.SUCCESS,
            )

    @admin.action(description="Установить приоритет 'Высокий'")
    def make_high_priority(self, request, queryset):
        updated = queryset.update(priority=Priority.HIGH)
        self.message_user(
            request,
            f"Обновлено ошибок: {updated}.",
            messages.SUCCESS,
        )

    actions = ("mark_closed", "make_high_priority")


admin.site.site_header = "Панель управления Freim"
admin.site.site_title = "Freim Bugtracker Admin"
admin.site.index_title = "Управление дефектами и справочниками"
