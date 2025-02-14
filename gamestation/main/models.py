from django.db import models

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
    tempo_segundo = models.PositiveIntegerField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=ATIVO)
    ultima_pausa = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Sessão {self.id} - {self.cliente}"


class CategoriaProduto(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    ATIVO = 1
    DESABILITADO = 0
    STATUS_CHOICES = [
        (ATIVO, 'Ativo'),
        (DESABILITADO, 'Desabilitado'),
    ]

    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    quantidade_estoque = models.PositiveIntegerField()
    categoria = models.ForeignKey(CategoriaProduto, on_delete=models.SET_NULL, blank=True, null=True, related_name="produtos")
    status = models.IntegerField(choices=STATUS_CHOICES, default=ATIVO)

    def __str__(self):
        return self.nome


class FormaPagamento(models.Model):
    ATIVO = 1
    DESABILITADO = 0
    STATUS_CHOICES = [
        (ATIVO, 'Ativo'),
        (DESABILITADO, 'Desabilitado'),
    ]

    nome = models.CharField(max_length=50)
    status = models.IntegerField(choices=STATUS_CHOICES, default=ATIVO)

    def __str__(self):
        return self.nome


class Venda(models.Model):
    CANCELADA = 0
    APROVADA = 1
    STATUS_CHOICES = [
        (CANCELADA, 'Cancelada'),
        (APROVADA, 'Aprovada'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, blank=True, null=True, related_name="vendas")
    valor_total = models.DecimalField(max_digits=8, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=APROVADA)
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"Venda {self.id} - {self.valor_total}"
    

class VendaItens(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, blank=True, null=True)
    quantidade = models.IntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=6, decimal_places=2)