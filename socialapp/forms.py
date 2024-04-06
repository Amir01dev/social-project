from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=250, required=True, label="نام کاربری یا تلفن",
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=250, required=True, label="رمز عبور",
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=20, widget=forms.PasswordInput, label="password")
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput, label="repeat password")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("پسورد وارد شده با تاییده پسورد یکی نمی باشد")
        return cd['password2']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError("phones already exist!")
        return phone


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'bio', 'photo', 'job']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if User.objects.exclude(id=self.instance.id).filter(phone=phone).exists():
            raise forms.ValidationError("phones already exist!")
        return phone

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(id=self.instance.id).filter(username=username).exists():
            raise forms.ValidationError("username already exist!")
        return username


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ('پیشنهاد', 'پیشنهادات'),
        ('انتقاد', 'انتقادات'),
        ('گزارش', 'گزارشات')
    )
    name = forms.CharField(max_length=250, required=True, label="نام",
                           widget=forms.TextInput(attrs={'placeholder': 'نام و نام خانوداگی'}))
    phone = forms.CharField(max_length=11, required=True, label="شماره تلفن")
    email = forms.EmailField(required=True, label="ایمیل")
    message = forms.CharField(widget=forms.Textarea, label="متن پیام", required=True)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError("شماره تلفن باید عددی باشد")
            if len(phone) < 11:
                raise forms.ValidationError("شماره تلفن باید 11 رقم باشد")
            else:
                return phone


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'tags']
