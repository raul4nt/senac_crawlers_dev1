from django.db import models

class UF(models.Model):
    estado = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "UF"
        verbose_name_plural = "UFs"

    def __str__(self):
        return self.estado

class Site(models.Model):
    url = models.URLField(max_length=255)
    nome = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Site"
        verbose_name_plural = "Sites"

    def __str__(self):
        return self.nome

class User(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.nome

class Edital(models.Model):
    nome_banca = models.CharField(max_length=255)
    titulo = models.CharField(max_length=255)
    valor = models.FloatField(null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)
    link = models.URLField(max_length=255)
    uf = models.ForeignKey(UF, on_delete=models.SET_NULL, null=True, blank=True)
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Edital"
        verbose_name_plural = "Editais"

    def __str__(self):
        return self.titulo
