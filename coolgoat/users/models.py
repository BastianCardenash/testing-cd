from django.db import models

class CoolgoatUser(models.Model):
    email = models.CharField(max_length=255, primary_key=True)
    funds = models.IntegerField()

    def __str__(self):
        return self.email
    
