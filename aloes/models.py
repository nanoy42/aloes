"""
Model of aloes app
"""
from django.db import models


class GeneralPreferences(models.Model):
    """
    Store general preferences (home text in french and english)
    """
    home_text = models.TextField(
        blank=True,
        verbose_name="Texte d'accueil",
        help_text="Ce texte sera affiché sur la page d'accueil, avant les documents"
    )
    english_home_text = models.TextField(blank=True, verbose_name="Texte d'accueil (anglais)")
