"""REST serviss (Django REST Framework).

Serializer pārvērš modeli JSON formātā, ViewSet nodrošina GET/POST/PUT/DELETE,
router automātiski izveido adreses (/api/cvs/, /api/skills/ utt.).
"""
from rest_framework import serializers, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.routers import DefaultRouter

from .models import CV, Education, Experience, Language, Skill


# ---------- Serializers ----------
class CVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV
        fields = "__all__"
        read_only_fields = ["owner"]


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"


# ---------- ViewSets ----------
class CVViewSet(viewsets.ModelViewSet):
    serializer_class = CVSerializer

    def get_queryset(self):
        # tikai pieteikušā lietotāja CV
        return CV.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SectionViewSet(viewsets.ModelViewSet):
    """Kopīga klase CV sadaļām. Apakšklasēs norāda tikai modeli un serializeri."""

    model = None

    def get_queryset(self):
        return self.model.objects.filter(cv__owner=self.request.user)

    def check_cv(self, serializer):
        # neļaujam pievienot ierakstu svešai CV
        if serializer.validated_data["cv"].owner != self.request.user:
            raise PermissionDenied("Šī CV nav jūsu.")

    def perform_create(self, serializer):
        self.check_cv(serializer)
        serializer.save()

    def perform_update(self, serializer):
        self.check_cv(serializer)
        serializer.save()


class EducationViewSet(SectionViewSet):
    model = Education
    serializer_class = EducationSerializer


class ExperienceViewSet(SectionViewSet):
    model = Experience
    serializer_class = ExperienceSerializer


class SkillViewSet(SectionViewSet):
    model = Skill
    serializer_class = SkillSerializer


class LanguageViewSet(SectionViewSet):
    model = Language
    serializer_class = LanguageSerializer


# ---------- Adreses ----------
router = DefaultRouter()
router.register("cvs", CVViewSet, basename="cv")
router.register("educations", EducationViewSet, basename="education")
router.register("experiences", ExperienceViewSet, basename="experience")
router.register("skills", SkillViewSet, basename="skill")
router.register("languages", LanguageViewSet, basename="language")
