from django import forms
from .models import Aluno, Curso

class AlunosForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome_completo','cpf','curso','data_de_nascimento','image','forma_de_ingresso']

class AtualizarVinculoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['situacao','vinculo']

class EscolherCursoForm(forms.Form):
    curso = forms.ModelChoiceField(queryset=Curso.objects.all())
    