from django.db import migrations, models
import datetime

class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_alter_userchallenge_started_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userchallenge',
            name='started_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]
