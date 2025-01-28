from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

# Create your models here.

class BaseModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Age(models.TextChoices):
    MALE = "M", _("Male")
    FEMALE = "F", _("Female")
    OTHER = "O", _("Other")

class Candidate(BaseModel):
    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=Age, default=Age.OTHER)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)