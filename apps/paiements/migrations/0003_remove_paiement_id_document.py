from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("paiements", "0002_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="paiement",
            name="id_document",
        ),
    ]
