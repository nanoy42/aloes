"""Models of documents app."""
from django.db import models


class Document(models.Model):
    """Store a document."""
    name = models.CharField(max_length=255, verbose_name="Nom du document")
    english_name = models.CharField(
        max_length=255,
        verbose_name="Nom du document (anglais)",
        blank=True
    )
    document = models.FileField(verbose_name="Fichier")
    english_document = models.FileField(verbose_name="Fichier (anglais)", blank=True, null=True)
    description = models.TextField(verbose_name="Description", blank=True)
    english_description = models.TextField(verbose_name="Description (anglais)", blank=True)
    active = models.BooleanField(default=True, verbose_name="Actif")

    def __str__(self):
        return self.name
