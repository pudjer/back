# Generated by Django 4.1.7 on 2023-02-27 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_alter_relations_parent_karma'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='pre_karma',
            field=models.IntegerField(blank=True, db_index=True, editable=False, null=True),
        ),
    ]