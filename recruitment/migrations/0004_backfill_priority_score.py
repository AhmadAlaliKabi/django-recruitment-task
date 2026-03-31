from django.db import migrations


def backfill_priority_score(apps, schema_editor):
    Candidate = apps.get_model('recruitment', 'Candidate')
    Candidate.objects.filter(priority_score__isnull=True).update(priority_score=50)


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment', '0003_set_default_priority'),
    ]

    operations = [
        migrations.RunPython(backfill_priority_score),
    ]