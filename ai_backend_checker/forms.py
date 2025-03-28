from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from image_cropping import ImageCropWidget

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            # Create user profile and save profile picture if provided
            profile = user.profile
            if self.cleaned_data.get("profile_picture"):
                profile.profile_picture = self.cleaned_data["profile_picture"]
                profile.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cropping']
        widgets = {
            'cropping': ImageCropWidget(),
        }