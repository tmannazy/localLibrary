# Generated by Django 4.1.5 on 2023-02-13 14:34

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_language_alter_bookinstance_id_book_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='id',
            field=models.UUIDField(default=uuid.UUID('d3985f9d-c476-4447-ad31-630c6d801b1b'), help_text='Unique ID for this particular book across whole library', primary_key=True, serialize=False),
        ),
    ]
