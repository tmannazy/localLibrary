# Generated by Django 4.1.5 on 2023-02-17 14:09

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0014_alter_bookinstance_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='id',
            field=models.UUIDField(default=uuid.UUID('9af84d94-b87f-43cb-808c-3a84d107a8c6'), help_text='Unique ID for this particular book across whole library', primary_key=True, serialize=False),
        ),
    ]