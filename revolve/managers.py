from django.db import models


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='PB')
