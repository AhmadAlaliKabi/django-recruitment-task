from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='priority_score',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]