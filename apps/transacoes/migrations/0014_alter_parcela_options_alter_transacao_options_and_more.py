# Generated by Django 5.0.6 on 2024-07-12 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transacoes', '0013_parcela_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='parcela',
            options={'verbose_name': 'Parcela', 'verbose_name_plural': 'Parcelas'},
        ),
        migrations.AlterModelOptions(
            name='transacao',
            options={'verbose_name': 'Transacao', 'verbose_name_plural': 'Transacoes'},
        ),
        migrations.AlterModelOptions(
            name='transacaoparcelada',
            options={'verbose_name': 'TransacaoParcela', 'verbose_name_plural': 'TransacaoParceladas'},
        ),
        migrations.AlterModelTable(
            name='parcela',
            table='parcela',
        ),
        migrations.AlterModelTable(
            name='transacao',
            table='transacao',
        ),
        migrations.AlterModelTable(
            name='transacaoparcelada',
            table='tansacao_parcelada',
        ),
    ]
