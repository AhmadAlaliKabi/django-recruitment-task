from django.db import migrations


def set_default_priority(apps, schema_editor):
    Candidate = apps.get_model('recruitment', 'Candidate')
    Candidate.objects.filter(priority_score__isnull=True).update(priority_score=50)


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment', '0002_candidate_priority_score'),
    ]

    operations = [
        migrations.RunPython(set_default_priority),
    ]