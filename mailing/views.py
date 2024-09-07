from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView, TemplateView

from blog.services import get_articles_from_cache
from mailing.forms import ClientForm, MessageForm, MailingForm, MailingManagerForm
from mailing.models import Client, Message, Mailing, Log


class HomeView(TemplateView):
    template_name = 'mailing/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailings = Mailing.objects.all()
        clients = Client.objects.all()
        context['mailings'] = mailings.count()
        context['active_mailings'] = mailings.filter(status=Mailing.STARTED).count()
        context['unique_clients'] = clients.values('email').distinct().count()
        context['random_blog'] = get_articles_from_cache().order_by('?')[:3]
        return context


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self, queryset=None):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_superuser and not user.grops.filter(name='manager'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser or self.request.user == self.object.owner:
            return self.object
        else:
            raise PermissionDenied


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        client = form.save(commit=False)
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def get_success_url(self):
        return reverse('mailing:client_detail', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser or self.request.user == self.object.owner:
            return self.object
        else:
            raise PermissionDenied


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser or self.request.user == self.object.owner:
            return self.object
        else:
            raise PermissionDenied


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self, queryset=None):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name='manager'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser or self.request.user == self.object.owner:
            return self.object
        else:
            raise PermissionDenied


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        message = form.save(commit=False)
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def get_success_url(self):
        return reverse('mailing:message_detail', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser or self.request.user == self.object.owner:
            return self.object
        else:
            raise PermissionDenied


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser or self.request.user == self.object.owner:
            return self.object
        else:
            raise PermissionDenied


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_queryset(self, queryset=None):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name='manager'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if user.is_superuser or user == self.object.owner or user.groups.filter(name='manager'):
            return self.object
        else:
            raise PermissionDenied


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        mailing = form.save(commit=False)
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_success_url(self):
        return reverse('mailing:mailing_detail', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        user = self.request.user
        if user.is_superuser or user == self.object.owner:
            return MailingForm
        elif user.has_perm('mailing.cancel_mailings'):
            return MailingManagerForm
        else:
            raise PermissionDenied


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser or self.request.user == self.object.owner:
            return self.object
        else:
            raise PermissionDenied


class LogListView(LoginRequiredMixin, ListView):
    model = Log
