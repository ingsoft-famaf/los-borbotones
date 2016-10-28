from django import forms

from .models import Video


class UploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['description'].widget.attrs = {
            'class': 'form-control'
        }


    class Meta:
        model = Video
        fields = ('title','description', 'file', )

