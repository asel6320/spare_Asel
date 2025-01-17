# Generated by Django 5.0.6 on 2024-11-19 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("webapp", "0024_alter_engine_displacement"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vehicleinfo",
            name="vehicle_type",
            field=models.CharField(
                choices=[
                    ("passenger", "Легковые автомобили"),
                    ("truck", "Грузовые автомобили"),
                    ("special", "Спецтехника"),
                    ("bus", "Автобусы"),
                    ("bicycle", "Мотоциклы"),
                ],
                max_length=50,
            ),
        ),
    ]
