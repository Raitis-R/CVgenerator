from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),

    # CV
    path("cv/", views.cv_list, name="cv_list"),
    path("cv/new/", views.cv_create, name="cv_create"),
    path("cv/<int:pk>/", views.cv_detail, name="cv_detail"),
    path("cv/<int:pk>/edit/", views.cv_edit, name="cv_edit"),
    path("cv/<int:pk>/delete/", views.cv_delete, name="cv_delete"),
    path("cv/<int:pk>/preview/", views.cv_preview, name="cv_preview"),

    # Izglītība
    path("cv/<int:cv_id>/education/add/", views.education_add, name="education_add"),
    path("education/<int:pk>/edit/", views.education_edit, name="education_edit"),
    path("education/<int:pk>/delete/", views.education_delete, name="education_delete"),

    # Darba pieredze
    path("cv/<int:cv_id>/experience/add/", views.experience_add, name="experience_add"),
    path("experience/<int:pk>/edit/", views.experience_edit, name="experience_edit"),
    path("experience/<int:pk>/delete/", views.experience_delete, name="experience_delete"),

    # Prasmes
    path("cv/<int:cv_id>/skill/add/", views.skill_add, name="skill_add"),
    path("skill/<int:pk>/edit/", views.skill_edit, name="skill_edit"),
    path("skill/<int:pk>/delete/", views.skill_delete, name="skill_delete"),

    # Valodas
    path("cv/<int:cv_id>/language/add/", views.language_add, name="language_add"),
    path("language/<int:pk>/edit/", views.language_edit, name="language_edit"),
    path("language/<int:pk>/delete/", views.language_delete, name="language_delete"),
]
