from django import forms
from models import Message

class MessageForm(forms.ModelForm):
    content_text = forms.CharField(required=True)

    class Meta:
        model = Message
        fields = ('content_text',)
