# Generated by Django 4.1.4 on 2023-01-03 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_customuser_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=10.0, max_digits=7),
        ),
    ]
