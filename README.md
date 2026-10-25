# CV ģenerators (Django, vienkāršā versija)

Lietotājs reģistrējas, izveido CV, pievieno izglītību, darba pieredzi, prasmes un valodas,
izvēlas dizainu un saglabā CV kā PDF (drukāšanas dialogs pārlūkā).

## Palaišana (Anaconda Prompt)

```bat
conda create -n cvgen python=3.12 -y
conda activate cvgen

cd C:\ceļš\līdz\cv_simple
pip install -r requirements.txt

python manage.py makemigrations cvapp
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

| Adrese | Kas tur ir |
|---|---|
| http://127.0.0.1:8000/ | sākumlapa |
| http://127.0.0.1:8000/register/ | reģistrācija |
| http://127.0.0.1:8000/cv/ | mani CV |
| http://127.0.0.1:8000/admin/ | CMS (admin panelis) |
| http://127.0.0.1:8000/api/ | REST serviss |

## Faili un ko tie dara

| Fails | Ko dara |
|---|---|
| `cvapp/models.py` | 5 tabulas: CV, Education, Experience, Skill, Language |
| `cvapp/forms.py` | formas, kas uzbūvētas no modeļiem |
| `cvapp/views.py` | funkcijas, kas apstrādā lapas (CRUD) |
| `cvapp/urls.py` | adreses → funkcijas |
| `cvapp/admin.py` | CMS konfigurācija |
| `cvapp/api.py` | REST serviss |
| `templates/base.html` | pamatšablons (navigācija, kājene) |
| `templates/cvapp/*.html` | lapas, kas mantojam no `base.html` |
| `static/` | CSS un JavaScript |

## Kritēriji

| Kritērijs | Kur |
|---|---|
| 20% – vismaz 5 DB tabulas | `cvapp/models.py` |
| 30% – vismaz 3 CRUD | `cvapp/views.py`: CV, izglītība, pieredze, prasmes, valodas (katrai pievienot / labot / dzēst / skatīt) |
| 10% – CMS | `cvapp/admin.py` |
| 10% – REST serviss | `cvapp/api.py` un `cvgenerator/urls.py` |
| 10% – šablonu mantošana | `{% extends "base.html" %}` visos šablonos |
| 10% – autorizācija | reģistrācija, ieeja, iziešana, `@login_required` |
| 10% – front-end projekts | `static/css`, `static/js` + Bootstrap. **Šeit jāieliek tavs kursa projekts**: savus CSS/JS/attēlus ieliec `static/`, lapas struktūru `templates/base.html` |

## REST piemērs

Pēc pieteikšanās pārlūkā atver `/api/cvs/`. Ar curl:

```bat
curl -u lietotajs:parole http://127.0.0.1:8000/api/cvs/
```
