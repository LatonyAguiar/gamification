from django.db import models
from django.contrib.auth.models import User

class Challenge(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    banner = models.ImageField(upload_to='banners/')
    scoring_rules = models.TextField()  # JSON or detailed description

    def __str__(self):
        return self.name

class Broker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11, unique=True)
    accepted_challenge = models.BooleanField(null=True, default=None)

    def __str__(self):
        return self.user.username

class ChallengeAssignment(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.broker} - {self.challenge}"
