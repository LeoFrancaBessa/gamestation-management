# Generated by Django 5.1.6 on 2025-02-12 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_sessao_ultima_pausa_delete_pausa'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sessao',
            old_name='tempo_minuto',
            new_name='tempo_segundo',
        ),
    ]
