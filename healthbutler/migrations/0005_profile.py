# Generated by Django 4.1.3 on 2022-12-14 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("healthbutler", "0004_questionandanswer_userinfo_checkin"),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("weight", models.IntegerField(default=0)),
                ("height", models.IntegerField(default=0)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="healthbutler.user",
                    ),
                ),
            ],
        ),
    ]
