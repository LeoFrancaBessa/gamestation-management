from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render
from django.views.generic import ListView
from .models import Sessao, TV, Cliente, Pausa
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
        data = json.loads(request.body)
        sessao_id = data.get('sessao_id')
        sessao = Sessao.objects.filter(id=sessao_id).first()
        if sessao and sessao.status == 1:
            sessao.status = 2
            sessao.save()
            pausa = Pausa.objects.create(sessao=sessao)
            return JsonResponse({
                'success': True,
                'message': 'Pausa criada com sucesso!',
                'id': pausa.id
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': "Sessão não existe ou não esta ativa"
            })


def retomar_sessao(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        sessao_id = data.get('sessao_id')
        sessao = Sessao.objects.filter(id=sessao_id).first()
        if sessao and sessao.status == 2:
            sessao.status = 1
            sessao.save()
            pausa = Pausa.objects.filter(sessao=sessao, fim=None)
            pausa.fim = timezone.now()
            pausa.save()
            return JsonResponse({
                'success': True,
                'message': 'Pausa finalizada com sucesso!',
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': "Sessão não existe ou não esta pausada"
            })