from django.db import models
from django.utils.html import format_html

from part.models import Part


class PartDocument(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name="documents")
    document = models.FileField(upload_to='documents/')
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Document for {self.part.name}"

    def to_display(self):
        return [
                self.description,
                self.part,
            ]

    def get_column_headers(self):
        return [
            'Описание',
            'Запчасть',
        ]


    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
