from django import forms
from .models import Aluno, Curso

class CPFFormatWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        if value is not None:
            value = '{}.{}.{}-{}'.format(value[:3], value[3:6], value[6:9], value[9:])
        return super().render(name, value, attrs=attrs, renderer=renderer)

class AlunosForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome_completo','cpf','curso','data_de_nascimento','image','forma_de_ingresso']
        cpf = forms.CharField(widget=CPFFormatWidget)
        
class AtualizarVinculoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['situacao','vinculo']

class EscolherCursoForm(forms.Form):
    curso = forms.ModelChoiceField(queryset=Curso.objects.all())
    