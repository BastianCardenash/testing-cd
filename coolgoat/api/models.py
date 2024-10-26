from django.db import models
from users.models import CoolgoatUser

class League(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    logo = models.URLField()
    flag = models.URLField()
    season = models.IntegerField()
    round = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.season}"
    
    
class Team(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    logo = models.URLField()
    winner = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class Match(models.Model):
    id = models.IntegerField(primary_key=True)
    referee = models.CharField(max_length=255, null=True, blank=True)
    timezone = models.CharField(max_length=255)
    date = models.DateTimeField()
    timestamp = models.IntegerField()
    status_long = models.CharField(max_length=255)
    status_short = models.CharField(max_length=10)
    elapsed = models.IntegerField(null=True, blank=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    home_team = models.ForeignKey(Team, related_name='home_matches', 
                                  on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_matches', 
                                  on_delete=models.CASCADE)
    goals_home = models.IntegerField(null=True, blank=True)
    goals_away = models.IntegerField(null=True, blank=True)
    bonds_available = models.IntegerField(default=40) 

    def __str__(self):
        return f"{self.home_team.name} vs {self.away_team.name} - {self.date}"
    

class Odds(models.Model):
    id_in_match = models.IntegerField()
    name = models.CharField(max_length=255)
    values = models.JSONField()
    match = models.ForeignKey(Match, on_delete=models.CASCADE, 
                              related_name='odds')

    def __str__(self):
        return f"Odds for {self.match}"

# falta agregar el id del usuario en el modelo (acordarse de borrar y crear la migracion de nuevo)
class Requests(models.Model):
    request_id = models.CharField(max_length=255, primary_key=True)
    group_id = models.CharField(max_length=255)
    fixture_id = models.IntegerField()
    league_name = models.CharField(max_length=255)
    round = models.CharField(max_length=255)
    date = models.DateTimeField()
    result = models.CharField(max_length=255)
    deposit_token = models.CharField(max_length=255)
    datetime = models.CharField(max_length=255)
    quantity = models.IntegerField()
    seller = models.IntegerField()
    wallet = models.BooleanField(default=True)
    validated = models.BooleanField(default=False)


class PastMatch(models.Model):
    id = models.IntegerField(primary_key=True)
    referee = models.CharField(max_length=255, null=True, blank=True)
    timezone = models.CharField(max_length=255)
    date = models.DateTimeField()
    timestamp = models.IntegerField()
    status_long = models.CharField(max_length=255)
    status_short = models.CharField(max_length=10)
    elapsed = models.IntegerField(null=True, blank=True)
    goals_home = models.IntegerField(null=True, blank=True)
    goals_away = models.IntegerField(null=True, blank=True)

    
class RequestUserRelation(models.Model):
    email = models.CharField(max_length=255)
    request_id = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.email} - {self.request_id}"

      
