from django.contrib import admin

from mailing.models import Client, Message, Mailing, Log


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'name',)
    search_fields = ('email', 'name',)
    list_filter = ('name', 'email',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'periodicity', 'start_date', 'end_date', 'owner')
    list_filter = ('status', 'periodicity', 'start_date', 'end_date')
    search_fields = ('name', 'status')


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('time', 'status', 'server_answer', 'mailing')
    list_filter = ('status', 'time')
    search_fields = ('status', 'time')
