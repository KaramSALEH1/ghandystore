from django.db import migrations, models

import item.models


class Migration(migrations.Migration):
    dependencies = [
        ("item", "0006_item_accent_hex"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="sizes",
            field=models.JSONField(
                blank=True,
                help_text='Optional list of sizes, e.g. ["S", "M", "L"]. Leave empty for no sizes.',
                null=True,
                validators=[item.models.validate_sizes],
            ),
        ),
    ]

