# Generated by Django 4.2 on 2023-11-07 12:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("teams", "0003_flag"),
    ]

    operations = [
        migrations.AddField(
            model_name="membership",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="The groups this membership belongs to. A membership  will get all permissions granted to each of their groups.",
                related_name="membership_set",
                related_query_name="membership",
                to="auth.group",
                verbose_name="Groups",
            ),
        ),
    ]
