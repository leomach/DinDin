# Generated by Django 5.1 on 2024-09-02 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transacoes', '0019_alter_transacao_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='transacao',
            name='cliente',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
