# Generated by Django 4.1.3 on 2022-12-14 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("healthbutler", "0010_checkin_questionandanswer_delete_userinfo"),
    ]

    operations = [

        migrations.RemoveField(model_name="checkin", name="user",),
        migrations.AddField(
            model_name="checkin",
            name="user_id",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
