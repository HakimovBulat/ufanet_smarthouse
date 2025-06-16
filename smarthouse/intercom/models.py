from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class House(models.Model):

    street = models.CharField("Улица", max_length=30)
    number = models.CharField("Номер дома", max_length=10)

    def __str__(self):
        return f"Дом {self.street}, {self.number}"
    
    class Meta:
        verbose_name = "Дом"
        verbose_name_plural = "Дома"
        ordering = ["id"]


class Apartment(models.Model):
    number = models.IntegerField("Номер квартиры", validators=[MaxValueValidator(1000), MinValueValidator(0)])
    house = models.ForeignKey(House, on_delete=models.CASCADE)

    def __str__(self):
        return f"Квартира {self.number}, {self.house}"
    
    class Meta:
        verbose_name = "Квартира"
        verbose_name_plural = "Квартиры"
        ordering = ["id"]


class Intercom(models.Model):
    name = models.CharField("Название", max_length=50)
    date_setup = models.DateField("Дата установки")
    house = models.ForeignKey(House, on_delete=models.CASCADE)

    def __str__(self):
        return f"Домофон {self.house}, {self.name}"

    class Meta:
        verbose_name = "Домофон"
        verbose_name_plural = "Домофоны"
        ordering = ["id"]