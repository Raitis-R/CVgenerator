from django.contrib.auth.models import User
from django.db import models

TEMPLATE_CHOICES = [
    ("classic", "Klasisks"),
    ("modern", "Moderns"),
    ("minimal", "Minimālistisks"),
]

SKILL_LEVELS = [
    (1, "Iesācējs"),
    (2, "Pamata"),
    (3, "Vidējs"),
    (4, "Labs"),
    (5, "Eksperts"),
]

LANGUAGE_LEVELS = [
    ("A1", "A1"),
    ("A2", "A2"),
    ("B1", "B1"),
    ("B2", "B2"),
    ("C1", "C1"),
    ("C2", "C2"),
    ("native", "Dzimtā valoda"),
]


# 1. tabula: CV
class CV(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cvs")
    title = models.CharField("CV profesijas nosaukums", max_length=120)
    full_name = models.CharField("Vārds, uzvārds", max_length=120)
    job_title = models.CharField("Vēlamais amats", max_length=120, blank=True)
    email = models.EmailField("E-pasts")
    phone = models.CharField("Tālrunis", max_length=30, blank=True)
    city = models.CharField("Pilsēta", max_length=80, blank=True)
    summary = models.TextField("Īss apraksts", blank=True)
    template = models.CharField("Dizains", max_length=20, choices=TEMPLATE_CHOICES, default="classic")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title


# 2. tabula: izglītība
class Education(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name="educations")
    institution = models.CharField("Mācību iestāde", max_length=150)
    degree = models.CharField("Kvalifikācija", max_length=150)
    start_year = models.IntegerField("Sākuma gads")
    end_year = models.IntegerField("Beigu gads (var atstāt tukšu)", null=True, blank=True)

    class Meta:
        ordering = ["-start_year"]

    def __str__(self):
        return f"{self.degree}, {self.institution}"


# 3. tabula: darba pieredze
class Experience(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name="experiences")
    company = models.CharField("Uzņēmums", max_length=150)
    position = models.CharField("Amats", max_length=150)
    start_date = models.DateField("No")
    end_date = models.DateField("Līdz (var atstāt tukšu)", null=True, blank=True)
    description = models.TextField("Apraksts", blank=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.position}, {self.company}"


# 4. tabula: prasmes
class Skill(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField("Prasme", max_length=100)
    level = models.IntegerField("Līmenis", choices=SKILL_LEVELS, default=3)

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"


# 5. tabula: valodas
class Language(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name="languages")
    name = models.CharField("Valoda", max_length=60)
    level = models.CharField("Līmenis", max_length=10, choices=LANGUAGE_LEVELS, default="B1")

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"
