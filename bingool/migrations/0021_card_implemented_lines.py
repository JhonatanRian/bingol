# Generated by Django 4.1.4 on 2023-01-30 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bingool', '0020_ballsline_line_remove_card_balls_delete_ballscards_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='implemented_lines',
            field=models.BooleanField(default=False, verbose_name='Linhas implementadas'),
        ),
    ]
