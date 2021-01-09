import django
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


class Reservation(models.Model):
    user = models.ForeignKey(
        User,
        to_field='username',
        on_delete=models.CASCADE,
        null=True
    )
    office = models.ForeignKey(
        Office,
        on_delete=models.CASCADE,
        null=True
    )
    workplace = models.ForeignKey(
        Workplace,
        on_delete=models.CASCADE,
        null=True
    )
    initial_day = models.DateField(
        default=django.utils.timezone.now
    )
    reservation_ends = models.DateField(
        default=django.utils.timezone.now
    )
