from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("formula", "0016_race_weight"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="race",
            options={
                "ordering": ["weight"],
                "verbose_name": "race",
                "verbose_name_plural": "races",
            },
        ),
    ]
