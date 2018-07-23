from django.db import models

class GeneralPreferences(models.Model):
    homeText = models.TextField(blank = True, verbose_name="Texte d'accueil", help_text="Ce texte sera affiché sur la page d'accueil, avant les documents")
    english_homeText = models.TextField(blank=True, verbose_name="Texte d'accueil (anglais)")
