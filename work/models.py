from django.db import models

class Manager(models.Model):
    name = models.CharField(
        max_length=150,
    )

    class Meta:
        verbose_name = "管理者"
