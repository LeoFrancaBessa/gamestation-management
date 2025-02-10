# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Categoriasproduto(models.Model):
    idcategoriaproduto = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'categoriasproduto'


class Clientes(models.Model):
    idcliente = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    nick = models.CharField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=100, blank=True, null=True)
    datacriacao = models.DateField(blank=True, null=True, auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'clientes'


class Consoles(models.Model):
    idconsole = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    precomeia = models.FloatField()
    precohora = models.FloatField()
    status = models.IntegerField(db_comment='1- DISPONIVEL 2- DEFEITO 3- MANUTENÇÃO')
    precocompra = models.FloatField()

    class Meta:
        managed = False
        db_table = 'consoles'


class Produtos(models.Model):
    idproduto = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    preco = models.FloatField()
    qtdestoque = models.IntegerField()
    idcategoriaproduto = models.ForeignKey(to=Categoriasproduto, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'produtos'


class Tvs(models.Model):
    idtv = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    idconsole = models.ForeignKey(to=Consoles, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.IntegerField(db_comment='1- DISPONIVEL 2- DEFEITO -3 MANUTENÇÃO')
    marca = models.CharField(max_length=100, blank=True, null=True)
    polegadas = models.CharField(max_length=100, blank=True, null=True)
    precocompra = models.FloatField()

    class Meta:
        managed = False
        db_table = 'tvs'


class Sessao(models.Model):
    idsessao = models.AutoField(primary_key=True)
    idcliente = models.ForeignKey(to=Clientes, on_delete=models.SET_NULL, null=True, blank=True)
    idtv = models.ForeignKey(to=Tvs, on_delete=models.SET_NULL, blank=True, null=True)
    inicio = models.DateTimeField(auto_now_add=True)
    tempominuto = models.BigIntegerField()
    status = models.IntegerField(db_comment='0- FINALIZADO 1- ATIVO 2- PAUSADO')

    class Meta:
        managed = False
        db_table = 'sessao'

class Pausas(models.Model):
    idpausa = models.AutoField(primary_key=True)
    idsessão = models.ForeignKey(to=Sessao, on_delete=models.CASCADE)
    inicio = models.DateTimeField(auto_now_add=True)
    fim = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pausas'


class Vendas(models.Model):
    idvenda = models.AutoField(primary_key=True)
    idcliente = models.ForeignKey(to=Clientes, on_delete=models.SET_NULL, blank=True, null=True)
    idproduto = models.ForeignKey(to=Produtos, on_delete=models.SET_NULL, blank=True, null=True)
    quantidade = models.IntegerField()
    valortotal = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'vendas'
