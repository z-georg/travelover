from django import forms
from travel.models import Photo, Comment
from django.contrib.auth.models import User


class CreatePhotoForm(forms.ModelForm):
    city = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    country = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    title = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'class': 'form-control rounded-2'
    }))

    image_url = forms.FileInput(
        attrs={
            'class': 'custom-file-input'
        }
    )

    class Meta:
        model = Photo
        fields = ['city', 'country', 'title', 'description', 'image_url']


class DeletePhotoForm(CreatePhotoForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for (_, field) in self.fields.items():
            field.widget.attrs['disabled'] = True
            field.widget.attrs['readonly'] = True


class CommentPhotoForm(forms.ModelForm):
    comment = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'class': 'form-control rounded-2'
    }))

    class Meta:
        model = Comment
        fields = ['comment', ]


class DeleteComment(forms.ModelForm):
    comment = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'class': 'form-control rounded-2'
    }))

    class Meta:
        model = Comment
        fields = '__all__'


class EditComment(forms.ModelForm):
    comment = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'class': 'form-control rounded-2'
    }))

    class Meta:
        model = Comment
        fields = ['comment', ]
