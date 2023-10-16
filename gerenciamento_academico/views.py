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
        cursos = Curso.objects.all()
        contagem_alunos_geral = Aluno.objects.count()
        contagem_alunos_ativos = Aluno.objects.filter(vinculo=1).count()
        contagem_alunos_inativos = Aluno.objects.filter(vinculo=2).count()
        ids_cursos = list(Curso.objects.values_list('id',flat=True))
        valores_campus = [item[0] for item in CAMPUS_CHOICES]
        nome_campus = [item[1] for item in CAMPUS_CHOICES]
        lista_contadores_curso = []
        lista_contadores_campus = []
        for i in ids_cursos:
            curso = Curso.objects.get(id=i)
            contagem = Aluno.objects.filter(curso=curso).count()
            lista_contadores_curso.append(f'Numero de alunos de {curso}: {contagem}')
        for i in valores_campus:
            contagem = Aluno.objects.filter(curso__campus=i).count()
            lista_contadores_campus.append(f'Numero de alunos de {nome_campus[i-1]}: {contagem}')
        context['lista_contagem_alunos_por_cursos'] = lista_contadores_curso
        context['lista_contagem_alunos_por_campus'] = lista_contadores_campus
        context['contagem_alunos_geral'] = contagem_alunos_geral
        context['contagem_alunos_ativos'] = contagem_alunos_ativos
        context['contagem_alunos_inativos'] = contagem_alunos_inativos
        context['campus'] = CAMPUS_CHOICES
        context['situacao'] = SITUACAO_CHOICES
        context['cursos'] = cursos
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

