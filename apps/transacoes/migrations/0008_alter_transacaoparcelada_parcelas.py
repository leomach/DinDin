# Generated by Django 5.0.6 on 2024-06-10 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transacoes', '0007_parcela_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transacaoparcelada',
            name='parcelas',
            field=models.IntegerField(),
        ),
    ]
