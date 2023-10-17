from typing import Any
from django import http
from django.forms.models import BaseModelForm
from django.shortcuts import render,redirect
from .Forms import AlunosForm, AtualizarVinculoForm,EscolherCursoForm
from .models import Aluno,Curso,CAMPUS_CHOICES, SITUACAO_CHOICES
from django.views.generic.edit import FormView, UpdateView
from django.views.generic import ListView
from django.views import generic,View
from django.http import HttpResponse, HttpResponseRedirect
from .models.options import SITUACAO_CHOICES
import json

class AlunosFormView(FormView):
    template_name = "alunos.html"
    form_class = AlunosForm
    success_url = "/alunos/form"

    def form_valid(self,form=None):
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lista_de_objetos_curso = Curso.objects.all()

        contagem_alunos_geral = Aluno.objects.count()
        contagem_alunos_ativos = Aluno.objects.filter(vinculo=1).count()
        contagem_alunos_inativos = Aluno.objects.filter(vinculo=2).count()
        lista_alunos_ativos_inativos = [contagem_alunos_ativos,contagem_alunos_inativos]
        lista_numero_de_alunos_por_curso_apresentacao = []
        lista_numero_de_alunos_por_campus_apresentacao = []
        lista_numero_de_alunos_por_curso = []
        lista_numero_de_alunos_por_campus = []
        lista_nome_dos_cursos = []
        lista_nome_dos_campus = []

        for objeto_curso in lista_de_objetos_curso:
            numero_de_alunos_atual = Aluno.objects.filter(curso=objeto_curso.id).count()
            lista_numero_de_alunos_por_curso_apresentacao.append(f'Numero de alunos de {str(objeto_curso)}: {Aluno.objects.filter(curso=objeto_curso.id).count()}')
            lista_nome_dos_cursos.append(str(objeto_curso))
            lista_numero_de_alunos_por_curso.append(numero_de_alunos_atual)
        for campus_id, campus_name in CAMPUS_CHOICES:
            numero_de_alunos_atual = Aluno.objects.filter(curso__campus=campus_id).count()
            lista_numero_de_alunos_por_campus_apresentacao.append(f'Numero de alunos de {campus_name}: {numero_de_alunos_atual}')
            lista_nome_dos_campus.append(campus_name)
            lista_numero_de_alunos_por_campus.append(numero_de_alunos_atual)
        context['lista_alunos_ativos_inativos'] = json.dumps(lista_alunos_ativos_inativos)
        context['lista_nome_dos_cursos'] = json.dumps(lista_nome_dos_cursos)
        context['lista_numero_de_alunos_por_curso'] = json.dumps(lista_numero_de_alunos_por_curso)
        context['lista_nome_dos_campus'] = json.dumps(lista_nome_dos_campus)
        context['lista_numero_de_alunos_por_campus'] = json.dumps(lista_numero_de_alunos_por_campus)
        context['lista_numero_de_alunos_por_curso_apresentacao'] = lista_numero_de_alunos_por_curso_apresentacao
        context['lista_numero_de_alunos_por_campus_apresentacao'] = lista_numero_de_alunos_por_campus_apresentacao
        context['contagem_alunos_geral'] = contagem_alunos_geral
        context['contagem_alunos_ativos'] = contagem_alunos_ativos
        context['contagem_alunos_inativos'] = contagem_alunos_inativos
        context['campus'] = CAMPUS_CHOICES
        context['situacao'] = SITUACAO_CHOICES
        context['cursos'] = lista_de_objetos_curso
        return context
    
    def post(self,request):
        NovaSituacaoVinculo = request.POST.get('atualizar')
        SituacaoVinculo = NovaSituacaoVinculo.split(',')
        id = int(SituacaoVinculo[0])
        NovaSituacao = int(SituacaoVinculo[1])
        if int(SituacaoVinculo[1]) == 1:
            Aluno.objects.filter(id=id).update(vinculo=1)
            Aluno.objects.filter(id=id).update(situacao=NovaSituacao)
        else:
            Aluno.objects.filter(id=id).update(vinculo=2)
            Aluno.objects.filter(id=id).update(situacao=NovaSituacao)

        return redirect(request.get_full_path())

class FiltroListView(ListView):
    model = Aluno
    template_name = 'filtro_list.html'

    # def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

    #     curso


    #     qs = qs.filter()

    #     CAMPUS_CHOICES

        

    #     return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        url_atual = self.request.path
        id_da_url = self.kwargs.get('pk')
        if url_atual == '/alunos/list/curso/' + str(id_da_url) + '/':
            return Aluno.objects.filter(curso=Curso.objects.get(id=id_da_url)).filter(vinculo=1)  
        if url_atual == '/alunos/list/campus/' + str(id_da_url) + '/':
            return Aluno.objects.filter(curso__campus=id_da_url).filter(vinculo=1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_atual = self.request.path
        id_da_url = self.kwargs.get('pk')
        if url_atual == '/alunos/list/curso/' + str(id_da_url) + '/':
            inativos = Aluno.objects.filter(curso=Curso.objects.get(id=id_da_url)).filter(vinculo=2)
            contagem_alunos_geral = Aluno.objects.filter(curso=Curso.objects.get(id=id_da_url)).count()
            contagem_alunos_ativos = Aluno.objects.filter(curso=Curso.objects.get(id=id_da_url)).filter(vinculo=1).count()
            contagem_alunos_inativos = Aluno.objects.filter(curso=Curso.objects.get(id=id_da_url)).filter(vinculo=2).count()
        else:
            inativos = Aluno.objects.filter(curso__campus=id_da_url).filter(vinculo=2)
            contagem_alunos_geral = Aluno.objects.filter(curso__campus=id_da_url).count()
            contagem_alunos_ativos = Aluno.objects.filter(curso__campus=id_da_url).filter(vinculo=1).count()
            contagem_alunos_inativos = Aluno.objects.filter(curso__campus=id_da_url).filter(vinculo=2).count()
        context['inativos'] = inativos
        context['contagem_alunos_geral'] = contagem_alunos_geral
        context['contagem_alunos_ativos'] = contagem_alunos_ativos
        context['contagem_alunos_inativos'] = contagem_alunos_inativos
        context['situacao'] = SITUACAO_CHOICES                     
        return context
    
    def post(self,request,**kwargs):
        NovaSituacaoVinculo = request.POST.get('atualizar')
        SituacaoVinculo = NovaSituacaoVinculo.split(',')
        id = int(SituacaoVinculo[0])
        NovaSituacao = int(SituacaoVinculo[1])
        if int(SituacaoVinculo[1]) == 1:
            Aluno.objects.filter(id=id).update(vinculo=1)
            Aluno.objects.filter(id=id).update(situacao=NovaSituacao)
        else:
            Aluno.objects.filter(id=id).update(vinculo=2)
            Aluno.objects.filter(id=id).update(situacao=NovaSituacao)

        return redirect(request.get_full_path())

