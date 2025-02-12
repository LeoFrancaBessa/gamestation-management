from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render
from django.views.generic import ListView
from .models import Sessao, TV, Cliente
from .forms import SessaoForm
import json

class GerenciamentoSessoes(ListView):
    model = Sessao
    template_name = "main/sessoes_ativas_list.html"
    context_object_name = "sessoes"

    def get_queryset(self):
        return Sessao.objects.exclude(status=0)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tvs'] = TV.objects.filter(status=1)
        context['clientes'] = Cliente.objects.all()
        return context


def criar_sessao(request):
    if request.method == 'POST':
        form = SessaoForm(request.POST)
        if form.is_valid():
            sessao = form.save()
            return JsonResponse({
                'success': True,
                'message': 'Sessão criada com sucesso!',
                'id': sessao.id
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    else:
        form = SessaoForm()
    
    return render(request, 'main/sessoes_ativas_list.html', {'form': form})


def pausar_sessao(request):
    if request.method == 'POST':
        sessao_id = request.POST.get('sessao_id')
        sessao = Sessao.objects.filter(id=sessao_id).first()
        if sessao and sessao.status == 1:
            sessao.status = 2
            sessao.ultima_pausa = timezone.now()
            sessao.save()
            return JsonResponse({
                'success': True,
                'message': 'Pausa adicionada com sucesso!',
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': "Sessão não existe ou não esta ativa"
            })


def ativar_sessao(request):
    if request.method == 'POST':
        sessao_id = request.POST.get('sessao_id')
        sessao = Sessao.objects.filter(id=sessao_id).first()
        if sessao and sessao.status == 2:
            #adicionar tempo a sessao
            diferencaEmSegundos = timezone.now() - sessao.ultima_pausa
            sessao.status = 1
            sessao.tempo_segundo = sessao.tempo_segundo + diferencaEmSegundos.total_seconds()
            sessao.save()
            return JsonResponse({
                'success': True,
                'message': 'Pausa finalizada com sucesso!',
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': "Sessão não existe ou não esta pausada"
            })
        

def finalizar_sessao(request):
    if request.method == 'POST':
        sessao_id = request.POST.get('sessao_id')
        sessao = Sessao.objects.filter(id=sessao_id).first()
        if sessao and not sessao.status == 0:
            sessao.status = 0
            sessao.save()
            return JsonResponse({
                'success': True,
                'message': 'Sessão finalizada com sucesso!',
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': "Sessão não existe ou já está finalizada"
            })