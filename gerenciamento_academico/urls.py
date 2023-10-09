from django.urls import path
from . import views

app_name = "gerenciamento_academico"
urlpatterns = [
    path("form",views.AlunosFormView.as_view(),name="form"),
    path("list",views.ListarView.as_view(),name="lista"),
    path("list/curso/<int:pk>/",views.FiltroListView.as_view(),name="lista-curso"),
    path("list/campus/<int:pk>/",views.FiltroListView.as_view(),name="lista-campus"),
    path("list/atualizar/<int:pk>/<int:situ>",views.ListarView.as_view(),name="atualizar")
]
