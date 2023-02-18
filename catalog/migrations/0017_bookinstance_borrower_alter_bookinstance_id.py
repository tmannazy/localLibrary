# Generated by Django 4.1.5 on 2023-02-17 14:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0016_alter_bookinstance_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookinstance',
            name='borrower',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='id',
            field=models.UUIDField(default=uuid.UUID('7109171f-4a99-4e2e-b1ff-154e843fd551'), help_text='Unique ID for this particular book across whole library', primary_key=True, serialize=False),
        ),
    ]