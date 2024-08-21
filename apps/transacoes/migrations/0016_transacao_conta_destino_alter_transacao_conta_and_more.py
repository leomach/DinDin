# Generated by Django 5.1 on 2024-08-21 20:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conta', '0004_alter_conta_options_alter_conta_table'),
        ('transacoes', '0015_alter_transacao_categoria_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transacao',
            name='conta_destino',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conta_destino', to='conta.conta', verbose_name='conta_destino'),
        ),
        migrations.AlterField(
            model_name='transacao',
            name='conta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conta', to='conta.conta', verbose_name='conta'),
        ),
        migrations.AlterField(
            model_name='transacao',
            name='tipo',
            field=models.CharField(default='D', max_length=1),
        ),
    ]
