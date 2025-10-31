from django.db import models


class HighlightTexts(models.Model):
    text = models.CharField(
        max_length=250,
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.text)


class InclusiveTexts(models.Model):
    text = models.CharField(
        max_length=250,
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.text)


class ExclusiveTexts(models.Model):
    text = models.CharField(
        max_length=250,
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.text)


class WhatKnowModel(models.Model):
    text = models.CharField(
        max_length=250,
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.text)


class WhatBringModel(models.Model):
    text = models.CharField(
        max_length=300,
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.text)
