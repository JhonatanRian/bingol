# Generated by Django 4.1.4 on 2023-01-04 22:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bingool', '0008_alter_bingo_ball_drawn'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='match',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bingool.match'),
        ),
    ]
