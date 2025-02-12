from django.urls import path
from .views import GerenciamentoSessoes, criar_sessao, pausar_sessao, ativar_sessao, finalizar_sessao

urlpatterns = [
    path("", GerenciamentoSessoes.as_view(), name="gerenciar_sessoes"),
    path("sessao/criar_sessao", criar_sessao, name='criar-sessão'),
    path("sessao/pausar_sessao", pausar_sessao, name='pausar-sessão'),
    path("sessao/ativar_sessao", ativar_sessao, name='ativar-sessão'),
    path("sessao/finalizar_sessao", finalizar_sessao, name='finalizar-sessão'),
]