# Generated by Django 5.0.6 on 2024-11-10 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("contacts", "0002_contactrequest_email_contactrequest_first_name"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="contactrequest",
            options={"verbose_name": "Контакт", "verbose_name_plural": "Контакты"},
        ),
    ]