from django.db import migrations, models

import item.models


class Migration(migrations.Migration):
    dependencies = [
        ("item", "0005_itemcolor_hex_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="accent_hex",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Optional product accent color, e.g. #C79D4C",
                max_length=7,
                validators=[item.models.validate_optional_hex],
            ),
        ),
    ]
