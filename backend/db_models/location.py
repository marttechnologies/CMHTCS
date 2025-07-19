from django.db import models


class Region(models.Model):
    """
    Model representing a region in Ethiopia.
    """
    region = models.CharField(max_length=100, unique=True, verbose_name="Region Name")
    
    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Regions"
    
    def __str__(self):
        return self.region

class City(models.Model):
    """
    Model representing a city in Ethiopia.
    """
    region = models.ForeignKey('Region', on_delete=models.CASCADE, related_name='cities', verbose_name="Region")
    city = models.CharField(max_length=100, unique=True, verbose_name="City Name")
    
    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
    
    def __str__(self):
        return f"{self.city}, {self.region.region}"

# Location Related Kebele or Subcity 
class Kebele(models.Model):
    """
    Model representing a Kebele or subcity in Ethiopia.
    """
    city = models.ForeignKey('City', on_delete=models.CASCADE, related_name='kebeles', verbose_name="City")
    kebele = models.CharField(max_length=100, unique=True, verbose_name="Kebele Name")
    mender = models.IntegerField(verbose_name="Mender Number")
    
    
    class Meta:
        verbose_name = "Kebele or Subcity"
        verbose_name_plural = "Kebeles or Subcities"
    
    def __str__(self):
        return f"{self.kebele} Mender {self.mender} {self.city.city}"