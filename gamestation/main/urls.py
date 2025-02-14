from django.urls import path
from .views import GerenciamentoSessoes, GerenciamentoVendas, criar_sessao, pausar_sessao, ativar_sessao, finalizar_sessao, adicionar_tempo_sessao

urlpatterns = [
    path("", GerenciamentoSessoes.as_view(), name="gerenciar-sessoes"),
    path("sessao/criar_sessao", criar_sessao, name='criar-sessão'),
    path("sessao/pausar_sessao", pausar_sessao, name='pausar-sessão'),
    path("sessao/ativar_sessao", ativar_sessao, name='ativar-sessão'),
    path("sessao/finalizar_sessao", finalizar_sessao, name='finalizar-sessão'),
    path("sessao/adicionar_tempo_sessao", adicionar_tempo_sessao, name='adicionar-tempo-sessão'),

    path("vendas/", GerenciamentoVendas.as_view(), name="gerenciar-vendas"),
]