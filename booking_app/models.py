from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Office(models.Model):
    workplaces = models.IntegerField(
        default=5
    )


class Workplace(models.Model):
    office = models.ForeignKey(
        Office,
        on_delete=models.CASCADE,
        null=True
    )
    price = models.IntegerField(
        default=1000
    )
