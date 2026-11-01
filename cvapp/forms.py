from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import CV, Education, Experience, Language, Skill


# Reģistrācijas forma
class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="E-pasts")

    class Meta:
        model = User
        fields = ["username", "email"]


class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ["title", "full_name", "job_title", "email", "phone", "city", "summary", "template"]


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ["institution", "degree", "start_year", "end_year"]


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ["company", "position", "start_date", "end_date", "description"]
        # Kalendāra skats
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "end_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ["name", "level"]


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ["name", "level"]
