"""
Database menu module models.
"""

from decimal import Decimal

from django.db import models
from django.core.validators import (
    MinLengthValidator,
    MinValueValidator,
)


class Menu(models.Model):
    """Database menu model."""

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=500, blank=True)
    added_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)


class Dish(models.Model):
    """Database dish model."""

    menu = models.ForeignKey(
        "menu.Menu", on_delete=models.CASCADE, related_name="dishes"
    )
    name = models.CharField(max_length=255, validators=[MinLengthValidator(1)])
    description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    preparation_time = models.DurationField()
    is_vegetarian = models.BooleanField(default=False)
    added_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
