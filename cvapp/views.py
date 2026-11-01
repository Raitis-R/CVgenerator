from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.utils.text import slugify
from .pdf import build_cv_pdf

from .forms import (
    CVForm,
    EducationForm,
    ExperienceForm,
    LanguageForm,
    RegisterForm,
    SkillForm,
)
from .models import CV, TEMPLATE_CHOICES, Education, Experience, Language, Skill


# sākumlapa un reģistrācija
def home(request):
    return render(request, "home.html")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # uzreiz pieslēdzam
            return redirect("cv_list")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})

# CV

@login_required
def cv_list(request):  # READ: saraksts
    cvs = CV.objects.filter(owner=request.user)
    return render(request, "cvapp/cv_list.html", {"cvs": cvs})


@login_required
def cv_detail(request, pk):  # READ: viena CV
    cv = get_object_or_404(CV, pk=pk, owner=request.user)
    return render(request, "cvapp/cv_detail.html", {"cv": cv})


@login_required
def cv_preview(request, pk):  # tīrs CV skats drukāšanai / PDF
    cv = get_object_or_404(CV, pk=pk, owner=request.user)
    return render(
        request,
        "cvapp/cv_preview.html",
        {"cv": cv, "template_choices": TEMPLATE_CHOICES},
    )


@login_required
def cv_create(request):  # CREATE
    if request.method == "POST":
        form = CVForm(request.POST)
        if form.is_valid():
            cv = form.save(commit=False)
            cv.owner = request.user
            cv.save()
            messages.success(request, "CV izveidots.")
            return redirect("cv_detail", pk=cv.pk)
    else:
        form = CVForm()
    return render(request, "cvapp/form.html", {"form": form, "title": "Jauna CV", "back_url": "/cv/"})


@login_required
def cv_edit(request, pk): # update
    cv = get_object_or_404(CV, pk=pk, owner=request.user)
    if request.method == "POST":
        form = CVForm(request.POST, instance=cv)
        if form.is_valid():
            form.save()
            messages.success(request, "CV saglabāts.")
            return redirect("cv_detail", pk=cv.pk)
    else:
        form = CVForm(instance=cv)
    return render(request, "cvapp/form.html", {"form": form, "title": "Labot CV", "back_url": f"/cv/{cv.pk}/"})


@login_required
def cv_delete(request, pk):  # delete
    cv = get_object_or_404(CV, pk=pk, owner=request.user)
    if request.method == "POST":
        cv.delete()
        messages.success(request, "CV dzēsts.")
        return redirect("cv_list")
    return render(request, "cvapp/confirm_delete.html", {"obj": cv, "back_url": f"/cv/{cv.pk}/"})

# Izglītība

@login_required
def education_add(request, cv_id):
    cv = get_object_or_404(CV, pk=cv_id, owner=request.user)
    if request.method == "POST":
        form = EducationForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.cv = cv
            item.save()
            return redirect("cv_detail", pk=cv.pk)
    else:
        form = EducationForm()
    return render(request, "cvapp/form.html", {"form": form, "title": "Pievienot izglītību", "back_url": f"/cv/{cv.pk}/"})


@login_required
def education_edit(request, pk):
    item = get_object_or_404(Education, pk=pk, cv__owner=request.user)
    if request.method == "POST":
        form = EducationForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("cv_detail", pk=item.cv.pk)
    else:
        form = EducationForm(instance=item)
    return render(request, "cvapp/form.html", {"form": form, "title": "Labot izglītību", "back_url": f"/cv/{item.cv.pk}/"})


@login_required
def education_delete(request, pk):
    item = get_object_or_404(Education, pk=pk, cv__owner=request.user)
    if request.method == "POST":
        cv_pk = item.cv.pk
        item.delete()
        return redirect("cv_detail", pk=cv_pk)
    return render(request, "cvapp/confirm_delete.html", {"obj": item, "back_url": f"/cv/{item.cv.pk}/"})

# Darba pieredze

@login_required
def experience_add(request, cv_id):
    cv = get_object_or_404(CV, pk=cv_id, owner=request.user)
    if request.method == "POST":
        form = ExperienceForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.cv = cv
            item.save()
            return redirect("cv_detail", pk=cv.pk)
    else:
        form = ExperienceForm()
    return render(request, "cvapp/form.html", {"form": form, "title": "Pievienot darba pieredzi", "back_url": f"/cv/{cv.pk}/"})


@login_required
def experience_edit(request, pk):
    item = get_object_or_404(Experience, pk=pk, cv__owner=request.user)
    if request.method == "POST":
        form = ExperienceForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("cv_detail", pk=item.cv.pk)
    else:
        form = ExperienceForm(instance=item)
    return render(request, "cvapp/form.html", {"form": form, "title": "Labot darba pieredzi", "back_url": f"/cv/{item.cv.pk}/"})


@login_required
def experience_delete(request, pk):
    item = get_object_or_404(Experience, pk=pk, cv__owner=request.user)
    if request.method == "POST":
        cv_pk = item.cv.pk
        item.delete()
        return redirect("cv_detail", pk=cv_pk)
    return render(request, "cvapp/confirm_delete.html", {"obj": item, "back_url": f"/cv/{item.cv.pk}/"})

# Prasmes:

@login_required
def skill_add(request, cv_id):
    cv = get_object_or_404(CV, pk=cv_id, owner=request.user)
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.cv = cv
            item.save()
            return redirect("cv_detail", pk=cv.pk)
    else:
        form = SkillForm()
    return render(request, "cvapp/form.html", {"form": form, "title": "Pievienot prasmi", "back_url": f"/cv/{cv.pk}/"})


@login_required
def skill_edit(request, pk):
    item = get_object_or_404(Skill, pk=pk, cv__owner=request.user)
    if request.method == "POST":
        form = SkillForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("cv_detail", pk=item.cv.pk)
    else:
        form = SkillForm(instance=item)
    return render(request, "cvapp/form.html", {"form": form, "title": "Labot prasmi", "back_url": f"/cv/{item.cv.pk}/"})


@login_required
def skill_delete(request, pk):
    item = get_object_or_404(Skill, pk=pk, cv__owner=request.user)
    if request.method == "POST":
        cv_pk = item.cv.pk
        item.delete()
        return redirect("cv_detail", pk=cv_pk)
    return render(request, "cvapp/confirm_delete.html", {"obj": item, "back_url": f"/cv/{item.cv.pk}/"})

# Valodas:

@login_required
def language_add(request, cv_id):
    cv = get_object_or_404(CV, pk=cv_id, owner=request.user)
    if request.method == "POST":
        form = LanguageForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.cv = cv
            item.save()
            return redirect("cv_detail", pk=cv.pk)
    else:
        form = LanguageForm()
    return render(request, "cvapp/form.html", {"form": form, "title": "Pievienot valodu", "back_url": f"/cv/{cv.pk}/"})


@login_required
def language_edit(request, pk):
    item = get_object_or_404(Language, pk=pk, cv__owner=request.user)
    if request.method == "POST":
        form = LanguageForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("cv_detail", pk=item.cv.pk)
    else:
        form = LanguageForm(instance=item)
    return render(request, "cvapp/form.html", {"form": form, "title": "Labot valodu", "back_url": f"/cv/{item.cv.pk}/"})


@login_required
def language_delete(request, pk):
    item = get_object_or_404(Language, pk=pk, cv__owner=request.user)
    if request.method == "POST":
        cv_pk = item.cv.pk
        item.delete()
        return redirect("cv_detail", pk=cv_pk)
    return render(request, "cvapp/confirm_delete.html", {"obj": item, "back_url": f"/cv/{item.cv.pk}/"})

@login_required
def cv_pdf(request, pk):  # lejupielādē CV kā PDF failu
    cv = get_object_or_404(CV, pk=pk, owner=request.user)
    response = HttpResponse(build_cv_pdf(cv), content_type="application/pdf")
    filename = f"{slugify(cv.full_name) or 'cv'}-CV.pdf"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response