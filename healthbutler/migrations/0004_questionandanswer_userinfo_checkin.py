# Generated by Django 4.1.3 on 2022-12-12 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("healthbutler", "0003_alter_foodtypes_options_foods"),
    ]

    '''operations = [
        migrations.CreateModel(
            name="Userinfo",
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
                ("usernum", models.CharField(max_length=16)),
                ("passwd", models.CharField(max_length=32)),
                ("weight", models.IntegerField(default=0)),
                ("height", models.IntegerField(default=0)),
            ],
        ),
        '''
    '''migrations.CreateModel(
            name="CheckIn",
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
                ("user_id", models.PositiveIntegerField()),
                ("name", models.CharField(max_length=200)),
                ("check_in_day", models.PositiveIntegerField()),
                ("days", models.PositiveIntegerField()),
            ],
            options={"ordering": ("id",), "index_together": {("user_id", "name")},},
        ),
    ]'''