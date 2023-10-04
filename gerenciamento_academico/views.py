from typing import Any
from django.forms.models import BaseModelForm
from django.shortcuts import render
from .Forms import AlunosForm, AtualizarVinculoForm,EscolherCursoForm
from .models import Aluno,Curso
from django.views.generic.edit import FormView, UpdateView
from django.views.generic import ListView
from django.views import generic,View
from django.http import HttpResponse, HttpResponseRedirect
from .models.options import SITUACAO_CHOICES


class AlunosFormView(FormView):
    template_name = "alunos.html"
    form_class = AlunosForm
    success_url = "/alunos/form"

    def form_valid(self,form=None):
        print("Form valido")
        form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        cursos = Curso.objects.all
        context['cursos'] = cursos
        return context

class AtualizarVinculoView(UpdateView):
    model = Aluno
    form_class = AtualizarVinculoForm
    template_name = 'lista/aluno_list.html'
    success_url = '/'

    def form_invalid(self, form=None):
        print("invalido")
        print(form)
        return super().form_invalid(form)
    def form_valid(self,form=None):
        print("Form valido")
        form.save()
        return super().form_valid(form)
   
class ListarView(ListView):
    model = Aluno
    template_name = 'aluno_list.html'
    context_object_name = 'alunos'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = EscolherCursoForm()
        cursos = Curso.objects.all()
        context['form_curso'] = form
        context['cursos'] = cursos
        return context
    
    def get_queryset(self):
        url_atual = self.request.path
        id_da_url = self.kwargs.get('pk')
        print(id_da_url)
        print(url_atual)
        print('alunos/list/curso/' + str(id_da_url))
        if url_atual == '/alunos/list/curso/' + str(id_da_url) + '/':
            print('entrou')
            teste = Curso.objects.get(id=id_da_url)
            return Aluno.objects.filter(curso=teste)
        
        return Aluno.objects.all()


    # def get(self,request):
    #     form = EscolherCursoForm() 
    #     alunos = Aluno.objects.filter(ativo = True)
    #     alunos_cursos = request.GET.get('')
    #     context = {'alunos':alunos,'formcurso':form}
    #     return render(request,'lista/aluno_list.html',context)
    
# class AlunosDoCursoView(ListView):
#     model = Aluno
#     template_name = 'lista/aluno_list.html'
#     context_object_name = 'alunos_curso'

#     def get_queryset(self):
#         curso_selecionado  = self.request.GET.get('curso',None)

#         if curso_selecionado:
#             return Aluno.objects.filter(curso = curso_selecionado)
        
#         return Aluno.objects.none()
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form_curso'] = EscolherCursoForm()  # Adicione o formulário ao contexto
#         return context



