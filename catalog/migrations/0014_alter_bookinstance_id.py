# Generated by Django 4.1.5 on 2023-02-17 13:46

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0013_alter_bookinstance_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='id',
            field=models.UUIDField(default=uuid.UUID('5c724f85-4ce0-4fd2-92d5-4d135383f4e0'), help_text='Unique ID for this particular book across whole library', primary_key=True, serialize=False),
        ),
    ]