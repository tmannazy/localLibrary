# Generated by Django 4.1.5 on 2023-02-21 23:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0020_alter_author_options_alter_bookinstance_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='date_of_death',
            field=models.DateField(blank=True, null=True, verbose_name='died'),
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='id',
            field=models.UUIDField(default=uuid.UUID('03246af5-9c71-437b-9c7c-095e32fc3867'), help_text='Unique ID for this particular book across whole library', primary_key=True, serialize=False),
        ),
    ]
