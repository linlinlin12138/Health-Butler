# Generated by Django 4.1.3 on 2022-12-14 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("healthbutler", "0008_questionandanswer_alter_profile_height_and_more"),
    ]

    operations = [

        migrations.AlterField(
            model_name="profile",
            name="height",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="weight",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),

    ]
