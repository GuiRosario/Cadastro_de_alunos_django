# Generated by Django 4.1 on 2023-09-27 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento_academico', '0002_aluno_ativo_curso_ativo_alter_aluno_situacao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluno',
            name='forma_de_ingresso',
            field=models.IntegerField(choices=[(2, 'SISU'), (3, 'PSEnem'), (1, 'Vestibular')], verbose_name='Forma de Ingresso'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='situacao',
            field=models.IntegerField(choices=[(3, 'Jubilado'), (4, 'Evadido'), (2, 'Formado'), (1, 'Vinculado')], verbose_name='Sitação'),
        ),
        migrations.AlterField(
            model_name='curso',
            name='campus',
            field=models.IntegerField(choices=[(2, 'Porto Nacional'), (3, 'Arraias'), (1, 'Palmas'), (5, 'Gurupi'), (4, 'Miracema')], verbose_name='Campus'),
        ),
    ]
