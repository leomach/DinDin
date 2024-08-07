# Generated by Django 5.0.6 on 2024-06-04 12:36

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categorias', '0001_initial'),
        ('conta', '0002_alter_conta_descricao'),
        ('subcategorias', '0001_initial'),
        ('transacoes', '0003_alter_transacao_tipo'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TransacaoParcelada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(default=datetime.date.today)),
                ('descricao', models.CharField(max_length=255)),
                ('parcelas', models.DecimalField(decimal_places=2, max_digits=3)),
                ('valor_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tipo', models.CharField(choices=[('R', 'Receita'), ('D', 'Despesa')], max_length=1)),
                ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='categorias.categoria')),
                ('conta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conta.conta')),
                ('subcategoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='subcategorias.subcategoria')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
