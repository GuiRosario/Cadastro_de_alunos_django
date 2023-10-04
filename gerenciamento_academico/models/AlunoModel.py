from django.db import models
from .CursoModel import Curso
from .options import SITUACAO_CHOICES, INGRESSO_CHOICES, VINCULO_CHOICES
import datetime
class Aluno(models.Model):
    nome_completo = models.CharField(max_length=500, verbose_name="Nome Completo")
    cpf = models.CharField(max_length=11, verbose_name="CPF")
    matricula = models.IntegerField(null=True,default=0,verbose_name="Mátricula")
    curso = models.ForeignKey(Curso,on_delete=models.RESTRICT, null=True,verbose_name="Curso")
    data_de_nascimento = models.DateField(verbose_name="Data de Nascimento")
    image = models.ImageField(upload_to='images/',verbose_name="Imagem do Aluno")
    situacao = models.IntegerField(choices=SITUACAO_CHOICES, verbose_name="Sitação",default=1)
    forma_de_ingresso = models.IntegerField(choices=INGRESSO_CHOICES, verbose_name="Forma de Ingresso")
    data_de_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Regitro")
    data_de_atualização = models.DateTimeField(auto_now=True,verbose_name="Data da Última <odificação")
    ativo = models.BooleanField(default=True)
    vinculo = models.IntegerField(choices=VINCULO_CHOICES, default=1)
    
    def __str__(self):
        return self.nome_completo
    
    def save(self, *args, **kwargs):
        Q_Verificar_Aluno = Aluno.objects.filter(id=self.id)
        if Q_Verificar_Aluno:
            pass
        else:    
            ano = datetime.datetime.now().year
            ano = str(ano)
            print(ano)
            if datetime.datetime.now().month < 7:
                ano = ano + '1'
            else:
                ano = ano + '2'
            total_objetos = Aluno.objects.count()
            if total_objetos == 0:
                self.matricula = int(ano + '0000')
            else: 
                objetos_ordenados = Aluno.objects.order_by('id')
                print(objetos_ordenados)
                objeto_recente = objetos_ordenados.last()
                codigo = objeto_recente.matricula + 1
                codigo = str(codigo)[5:]
                codigo = ano + str(codigo)
                print(codigo)
                self.matricula = int(codigo)
                
        super(Aluno, self).save(*args, **kwargs)  # Call the parent class's save() method