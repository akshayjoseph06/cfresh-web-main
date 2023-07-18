from django.db import models
from ckeditor.fields import RichTextField


class Link(models.Model):
    ios = models.CharField(max_length=255)
    android = models.CharField(max_length=255)

    class Meta:
        db_table = 'cfresh_link'
        verbose_name = 'link'
        verbose_name_plural = 'links'
        ordering = ["-id"]

    def __str__(self):
        return self.android


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    mob = models.BigIntegerField()
    message = models.TextField()


    class Meta:
        db_table = 'cfresh_contact'
        verbose_name = 'contact'
        verbose_name_plural = 'contacts'
        ordering = ["-id"]

    def __str__(self):
        return self.name



class Privacy(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextField()


    class Meta:
        db_table = 'cfresh_privacy'
        verbose_name = 'privacy'
        verbose_name_plural = 'privacy'
        ordering = ["-id"]

    def __str__(self):
        return self.title


class About(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextField()


    class Meta:
        db_table = 'cfresh_about'
        verbose_name = 'about'
        verbose_name_plural = 'abouts'
        ordering = ["-id"]

    def __str__(self):
        return self.title



class Terms(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextField()


    class Meta:
        db_table = 'cfresh_terms'
        verbose_name = 'terms'
        verbose_name_plural = 'terms'
        ordering = ["-id"]

    def __str__(self):
        return self.title



class Return(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextField()


    class Meta:
        db_table = 'cfresh_return'
        verbose_name = 'return'
        verbose_name_plural = 'return'
        ordering = ["-id"]

    def __str__(self):
        return self.title