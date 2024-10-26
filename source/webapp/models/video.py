# from django.db import models
#
#
# class Video(models.Model):
#     title = models.CharField(max_length=100)
#     video_file = models.FileField(upload_to='videos/', verbose_name='Video file', null=True, blank=True)
#
#     def __str__(self):
#         return f'Название видео - {self.title}. Его файл - {self.video_file}'
#
#     class Meta:
#         verbose_name = 'Video'
#         verbose_name_plural = 'Videos'
#         ordering = ['title']
#         db_table = 'video'
