from django.urls import path
from .views import GerenciamentoSessoes, criar_sessao

urlpatterns = [
    path("", GerenciamentoSessoes.as_view(), name="gerenciar_sessoes"),
    path("sessao/criar_sessao", criar_sessao, name='criar-sessão'),
]