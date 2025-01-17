# Generated by Django 5.0.6 on 2024-10-24 09:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('part', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='documents/')),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='part.part')),
            ],
            options={
                'verbose_name': 'Документ',
                'verbose_name_plural': 'Документы',
            },
        ),
    ]
