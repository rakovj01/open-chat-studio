# Generated by Django 4.2.7 on 2023-12-20 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("analysis", "0007_alter_analysisrun_status_alter_rungroup_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="rungroup",
            name="created_by",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="rungroup",
            name="approved",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="rungroup",
            name="notes",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="rungroup",
            name="starred",
            field=models.BooleanField(default=False),
        ),
    ]
