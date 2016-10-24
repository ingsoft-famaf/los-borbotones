from django import forms

from .models import Video


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('title','description', 'file', )

	class Media:
		css = {
			'all': ('style.css',)
		}
