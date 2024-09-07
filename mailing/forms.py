from django import forms

from mailing.models import Client, Mailing, Message


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('owner',)


class MailingForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Mailing
        exclude = ('owner', 'status',)
        widgets = {
            'start_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}),
            'next_send_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}),
        }


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('owner',)

    def clean_title(self):
        cleaned_data = self.cleaned_data['title']
        banned_words = ['казино', 'криптовалюта', 'крипта', 'биржа', ' дешево', 'бесплатно', 'обман', 'полиция',
                        'радар']
        for banned_word in banned_words:
            if banned_word in cleaned_data.lower():
                raise forms.ValidationError(f'Нельзя использовать слово "{banned_word}" для заголовка')
        return cleaned_data

    def clean_text(self):
        cleaned_data = self.cleaned_data['text']
        banned_words = ['казино', 'криптовалюта', 'крипта', 'биржа', ' дешево', 'бесплатно', 'обман', 'полиция',
                        'радар']
        for banned_word in banned_words:
            if banned_word in cleaned_data.lower():
                raise forms.ValidationError(f'Нельзя использовать слово "{banned_word}" для сообщения')
        return cleaned_data


class MailingManagerForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('status',)
