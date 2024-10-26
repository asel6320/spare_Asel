from django.db import models

from part.models import Part


class PartDocument(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name="documents")
    document = models.FileField(upload_to='documents/')
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Document for {self.part.name}"

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
