from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render
from django.views.generic import ListView
from .models import Sessao, TV, Cliente, Venda, Produto
from .forms import SessaoForm
from .utils import sessao_acabada

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
    

class GerenciamentoVendas(ListView):
    model = Sessao
    template_name = "main/vendas_list.html"
    context_object_name = "vendas"

    def get_queryset(self):
        return Venda.objects.all()


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
        

def adicionar_tempo_sessao(request):
    if request.method == 'POST':
        sessao_id = request.POST.get('sessao_id')
        tempo = request.POST.get('tempo')
        tipo = request.POST.get('tipo')
        tempo_segundo = int(tempo) * 60 if tipo == 'minuto' else int(tempo) * 3600
        sessao = Sessao.objects.filter(id=int(sessao_id)).first()
        if sessao:
            #Sessao finalizada, atualiza o tempo, atualiza o status e atualiza o tempo de inicio
            if sessao_acabada(sessao.inicio, sessao.tempo_segundo):
                sessao.tempo_segundo = tempo_segundo
                sessao.status = 1
                sessao.inicio = timezone.now()
            #Sessao em andamento, somente adiciona o tempo
            else:
                sessao.tempo_segundo += tempo_segundo
            sessao.save()
            return JsonResponse({
                'success': True,
                'message': 'Tempo adicionado com sucesso!',
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': "Sessão não existe"
            })