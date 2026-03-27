import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formula', '0026_profile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='circuit',
            options={'ordering': ['weight'], 'verbose_name': 'circuit', 'verbose_name_plural': 'circuits'},
        ),
        migrations.AlterModelOptions(
            name='constructor',
            options={'ordering': ['weight'], 'verbose_name': 'constructor', 'verbose_name_plural': 'constructors'},
        ),
        migrations.AddField(
            model_name='circuit',
            name='weight',
            field=models.PositiveIntegerField(db_index=True, default=0, verbose_name='weight'),
        ),
        migrations.AddField(
            model_name='constructor',
            name='weight',
            field=models.PositiveIntegerField(db_index=True, default=0, verbose_name='weight'),
        ),
    ]
