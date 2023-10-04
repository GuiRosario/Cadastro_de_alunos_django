# Generated by Django 4.1 on 2023-09-27 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento_academico', '0013_alter_aluno_forma_de_ingresso_alter_aluno_situacao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluno',
            name='situacao',
            field=models.IntegerField(choices=[(1, 'Vinculado'), (2, 'Formado'), (4, 'Evadido'), (3, 'Jubilado')], verbose_name='Sitação'),
        ),
        migrations.AlterField(
            model_name='curso',
            name='campus',
            field=models.IntegerField(choices=[(2, 'Porto Nacional'), (3, 'Arraias'), (1, 'Palmas'), (5, 'Gurupi'), (4, 'Miracema')], verbose_name='Campus'),
        ),
    ]
