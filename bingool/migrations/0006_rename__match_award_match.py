# Generated by Django 4.1.4 on 2023-01-04 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bingool', '0005_bot_bingo_standby_alter_ball_number_alter_card_balls_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='award',
            old_name='_match',
            new_name='match',
        ),
    ]