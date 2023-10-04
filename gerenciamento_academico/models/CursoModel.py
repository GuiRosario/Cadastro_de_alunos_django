from django.db import models
from .options import CAMPUS_CHOICES

class Curso(models.Model):
    nome = models.CharField(max_length=500,verbose_name="Nome do Curso")
    campus = models.IntegerField(choices=CAMPUS_CHOICES,verbose_name="Campus")
    data_de_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Registor")
    data_de_atualização = models.DateTimeField(auto_now=True, verbose_name="Data da última modificação")
    ativo = models.BooleanField(default=True)
    def __str__(self):
        valor_chave = self.campus
        for key, campus in CAMPUS_CHOICES:
            if key == valor_chave:
                campus_selecionado = campus
                break

        return str(str(self.nome) + '-' + campus_selecionado)