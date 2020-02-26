from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Image

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UploadPicForm(forms.Form):
    image_field = forms.CharField(required=False)
    file_field = forms.FileField(label='Or ', required=False)
    caption_field = forms.CharField(label='Caption ', max_length=100)

    def clean(self):
        cleaned_data = super(UploadPicForm, self).clean()
        if cleaned_data['image_field'] and cleaned_data['file_field']:
            raise forms.ValidationError('Please select either take picture or upload picture')
        if not cleaned_data['image_field'] and not cleaned_data['file_field']:
            raise forms.ValidationError('Please fill in one of fields.')
        return cleaned_data

class NotificationForm(forms.Form):
    notification = forms.BooleanField(
        label="Do you want notification when someone commented on your post?",
        required=False,
        initial=True,
    )