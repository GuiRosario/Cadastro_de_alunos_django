from typing import Any
from django.forms.models import BaseModelForm
from django.shortcuts import render,redirect
from .Forms import AlunosForm, AtualizarVinculoForm,EscolherCursoForm
from .models import Aluno,Curso,CAMPUS_CHOICES, SITUACAO_CHOICES
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
    
class ListarView(ListView):
    model = Aluno
    template_name = 'aluno_list.html'
    context_object_name = 'alunos'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cursos = Curso.objects.all()
        context['cursos'] = cursos
        context['campus'] = CAMPUS_CHOICES
        context['situacao'] = SITUACAO_CHOICES
        return context
    
    def post(self,request):
        teste = request.POST.get('atualizar')
        partes = teste.split(',')
        id = int(partes[0])
        situ = int(partes[1])
        if int(partes[1]) == 1:
            Aluno.objects.filter(id=id).update(vinculo=1)
            Aluno.objects.filter(id=id).update(situacao=situ)
        else:
            Aluno.objects.filter(id=id).update(vinculo=2)
            Aluno.objects.filter(id=id).update(situacao=situ)

        return redirect(request.get_full_path())
    # def get_queryset(self):
    #     url_atual = self.request.path
    #     id_da_url = self.kwargs.get('pk')
    #     situ_url = self.kwargs.get('situ')
    #     print(id_da_url)
    #     print(url_atual)
    #     print('alunos/list/curso/' + str(id_da_url))
    #     if url_atual == '/alunos/list/atualizar/' + str(id_da_url) + '/' + str(situ_url):
    #         print("entrou situ")
    #         if situ_url == 1:
    #             Aluno.objects.filter(id=id_da_url).update(vinculo=1)
    #             Aluno.objects.filter(id=id_da_url).update(situacao=situ_url)
    #         else:
    #             Aluno.objects.filter(id=id_da_url).update(vinculo=2)
    #             Aluno.objects.filter(id=id_da_url).update(situacao=situ_url)
    #         return Aluno.objects.all()
    #     return Aluno.objects.all()
    
    # def get_queryset(self):
    #     url_atual = self.request.path
    #     id_da_url = self.kwargs.get('pk')
    #     print(id_da_url)
    #     print(url_atual)
    #     print('alunos/list/curso/' + str(id_da_url))
    #     if url_atual == '/alunos/list/curso/' + str(id_da_url) + '/':
    #         print('entrou')
    #         teste = Curso.objects.get(id=id_da_url)
    #         return Aluno.objects.filter(curso=teste)
        
    #     return Aluno.objects.all()

class FiltroListView(ListView):
    model = Aluno
    template_name = 'filtro_list.html'
    context_object_name = 'alunos'

    def get_queryset(self):
        url_atual = self.request.path
        id_da_url = self.kwargs.get('pk')
        print(id_da_url)
        print(url_atual)
        print('alunos/list/curso/' + str(id_da_url))
        if url_atual == '/alunos/list/curso/' + str(id_da_url) + '/':
            print('entrou')
            teste = Curso.objects.get(id=id_da_url)
            return Aluno.objects.filter(curso=teste).filter(vinculo=1)  
        if url_atual == '/alunos/list/campus/' + str(id_da_url) + '/':
            print('entrou campus')
            return Aluno.objects.filter(curso__campus=id_da_url).filter(vinculo=1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_atual = self.request.path
        id_da_url = self.kwargs.get('pk')
        context['situacao'] = SITUACAO_CHOICES
        if url_atual == '/alunos/list/curso/' + str(id_da_url) + '/':
            teste = Curso.objects.get(id=id_da_url)
            inativos = Aluno.objects.filter(curso=teste).filter(vinculo=2)
            context['inativos'] = inativos
        else:
            teste = Aluno.objects.filter(curso__campus=id_da_url)
            inativos = teste.filter(vinculo=2)
            context['inativos'] = inativos                 
        return context
    
    def post(self,request,**kwargs):
        teste = request.POST.get('atualizar')
        partes = teste.split(',')
        id = int(partes[0])
        situ = int(partes[1])
        if int(partes[1]) == 1:
            Aluno.objects.filter(id=id).update(vinculo=1)
            Aluno.objects.filter(id=id).update(situacao=situ)
        else:
            Aluno.objects.filter(id=id).update(vinculo=2)
            Aluno.objects.filter(id=id).update(situacao=situ)

        return redirect(request.get_full_path())
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



