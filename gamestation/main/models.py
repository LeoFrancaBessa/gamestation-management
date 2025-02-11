from django.db import models

class CategoriaProduto(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Cliente(models.Model):
    nome = models.CharField(max_length=100, blank=True, null=True)
    nick = models.CharField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    data_criacao = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nome or self.nick


class Console(models.Model):
    DISPONIVEL = 1
    DEFEITO = 2
    MANUTENCAO = 3
    STATUS_CHOICES = [
        (DISPONIVEL, 'Disponível'),
        (DEFEITO, 'Defeito'),
        (MANUTENCAO, 'Manutenção'),
    ]

    nome = models.CharField(max_length=100)
    preco_meia_hora = models.DecimalField(max_digits=6, decimal_places=2)
    preco_hora = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.IntegerField(choices=STATUS_CHOICES, default=DISPONIVEL)
    preco_compra = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome


class TV(models.Model):
    DISPONIVEL = 1
    DEFEITO = 2
    MANUTENCAO = 3
    STATUS_CHOICES = [
        (DISPONIVEL, 'Disponível'),
        (DEFEITO, 'Defeito'),
        (MANUTENCAO, 'Manutenção'),
    ]

    nome = models.CharField(max_length=100)
    console = models.ForeignKey(Console, on_delete=models.SET_NULL, blank=True, null=True, related_name="tvs")
    status = models.IntegerField(choices=STATUS_CHOICES, default=DISPONIVEL)
    marca = models.CharField(max_length=100, blank=True, null=True)
    polegadas = models.CharField(max_length=10, blank=True, null=True)
    preco_compra = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nome} - {self.marca}"


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    quantidade_estoque = models.PositiveIntegerField()
    categoria = models.ForeignKey(CategoriaProduto, on_delete=models.SET_NULL, blank=True, null=True, related_name="produtos")

    def __str__(self):
        return self.nome


class Sessao(models.Model):
    FINALIZADO = 0
    ATIVO = 1
    PAUSADO = 2
    STATUS_CHOICES = [
        (FINALIZADO, 'Finalizado'),
        (ATIVO, 'Ativo'),
        (PAUSADO, 'Pausado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, related_name="sessoes")
    tv = models.ForeignKey(TV, on_delete=models.SET_NULL, blank=True, null=True, related_name="sessoes")
    inicio = models.DateTimeField(auto_now_add=True)
    tempo_minuto = models.PositiveIntegerField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=ATIVO)

    def __str__(self):
        return f"Sessão {self.id} - {self.cliente}"


class Pausa(models.Model):
    sessao = models.ForeignKey(Sessao, on_delete=models.CASCADE, related_name="pausas")
    inicio = models.DateTimeField(auto_now_add=True)
    fim = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Pausa da Sessão {self.sessao.id}"


class Venda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, blank=True, null=True, related_name="vendas")
    sessao = models.ForeignKey(Sessao, on_delete=models.SET_NULL, blank=True, null=True, related_name="vendas")
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, blank=True, null=True, related_name="vendas")
    quantidade = models.PositiveIntegerField()
    valor_total = models.DecimalField(max_digits=8, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venda {self.id} - {self.valor_total}"