from django.utils import timezone
from datetime import timedelta

def sessao_acabada(sessao_inicio, sessao_tempo_segundo):
    agora = timezone.now()
    tempo_decorrido = sessao_inicio + timedelta(seconds=sessao_tempo_segundo)

    return tempo_decorrido >= agora
