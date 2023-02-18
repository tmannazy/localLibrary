# Generated by Django 4.1.5 on 2023-02-13 16:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_alter_bookinstance_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='id',
            field=models.UUIDField(default=uuid.UUID('6f5b0609-a94a-489d-9eed-123f2b9b22b3'), help_text='Unique ID for this particular book across whole library', primary_key=True, serialize=False),
        ),
    ]
