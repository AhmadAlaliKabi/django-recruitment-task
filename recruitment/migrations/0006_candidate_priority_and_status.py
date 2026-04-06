"""Adds candidate application_status and priority_score with data migration."""

from django.db import migrations, models


def set_priority_for_existing_candidates(apps, schema_editor):
    Candidate = apps.get_model("recruitment", "Candidate")
    Candidate.objects.filter(priority_score__isnull=True).update(priority_score=50)


class Migration(migrations.Migration):
    dependencies = [
        ("recruitment", "0005_dailystats"),
    ]

    operations = [
        migrations.AddField(
            model_name="candidate",
            name="application_status",
            field=models.CharField(
                choices=[("screening", "Screening"), ("interview", "Interview"), ("rejected", "Rejected")],
                default="screening",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="candidate",
            name="priority_score",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.RunPython(set_priority_for_existing_candidates, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="candidate",
            name="priority_score",
            field=models.PositiveIntegerField(default=50),
        ),
    ]
