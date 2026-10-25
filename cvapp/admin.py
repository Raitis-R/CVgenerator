"""CMS: Django administrēšanas panelis (/admin/).
Šeit reģistrējam modeļus, lai tos varētu pārvaldīt caur admin lapu.
"""
from django.contrib import admin

from .models import CV, Education, Experience, Language, Skill


# Inline = sadaļas var labot tieši CV lapā
class EducationInline(admin.TabularInline):
    model = Education
    extra = 0


class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 0


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 0


class LanguageInline(admin.TabularInline):
    model = Language
    extra = 0


@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = ["title", "full_name", "owner", "template", "updated_at"]  # kolonnas sarakstā
    list_filter = ["template"]                                                # filtrs sānā
    search_fields = ["title", "full_name", "email"]                           # meklēšana
    inlines = [EducationInline, ExperienceInline, SkillInline, LanguageInline]


admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Skill)
admin.site.register(Language)
