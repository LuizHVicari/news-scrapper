from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# not the best practice but using this the client does not need to populate the database
class MktOptions(models.TextChoices):
    ARGENTINA = 'es-AR', 'Argentina'
    AUSTRALIA = 'en-AU', 'Austrália'
    AUSTRIA = 'de-AT', 'Áustria'
    BELGIUM = 'nl-BE', 'Bélgica'
    BELGIUM_FR = 'fr-BE', 'Bélgica'
    BRAZIL = 'pt-BR', 'Brasil'
    CANADA = 'en-CA', 'Canadá'
    CANADA_FR = 'fr-CA', 'Canadá'
    CHILE = 'es-CL', 'Chile'
    DENMARK = 'da-DK', 'Dinamarca'
    FINLAND = 'fi-FI', 'Finlândia'
    FRANCE = 'fr-FR', 'França'
    GERMANY = 'de-DE', 'Alemanha'
    HONG_KONG_SAR = 'zh-HK', 'Hong Kong SAR'
    INDIA = 'en-IN', 'Índia'
    INDONESIA = 'en-ID', 'Indonésia'
    ITALY = 'it-IT', 'Itália'
    JAPAN = 'ja-JP', 'Japão'
    KOREA = 'ko-KR', 'Coreia'
    MALAYSIA = 'en-MY', 'Malásia'
    MEXICO = 'es-MX', 'México'
    NETHERLANDS = 'nl-NL', 'Países Baixos'
    NEW_ZEALAND = 'en-NZ', 'Nova Zelândia'
    NORWAY = 'no-NO', 'Noruega'
    PEOPLES_REPUBLIC_OF_CHINA = 'zh-CN', 'República Popular da China'
    POLAND = 'pl-PL', 'Polônia'
    REPUBLIC_OF_THE_PHILIPPINES = 'en-PH', 'Filipinas'
    RUSSIA = 'ru-RU', 'Rússia'
    SOUTH_AFRICA = 'en-ZA', 'África do Sul'
    SPAIN = 'es-ES', 'Espanha'
    SWEDEN = 'sv-SE', 'Suécia'
    SWITZERLAND = 'fr-CH', 'Suíça'
    SWITZERLAND_DE = 'de-CH', 'Suíça'
    TAIWAN = 'zh-TW', 'Taiwan'
    TURKIYE = 'tr-TR', 'Turquia'
    UNITED_KINGDOM = 'en-GB', 'Reino Unido'
    UNITED_STATES = 'en-US', 'Estados Unidos'
    UNITED_STATES_SPANISH = 'es-US', 'Estados Unidos'


class FreshnessOptions(models.TextChoices):
    DAY = 'Day', 'Dia'
    MONTH = 'Month', 'Mês'
    YEAR = 'Year', 'Ano'

class Query(models.Model):

    class Meta:
        verbose_name = 'Busca'
        verbose_name_plural = 'Buscas'
        constraints = [
            models.UniqueConstraint(fields=['query_term', 'mkt'], name='query term and mkt must be unique together')
        ]

    query_term = models.CharField(max_length=100,
                                  verbose_name='termo de busca',
                                  help_text='Palavra(s) chave da busca')
    count = models.IntegerField(default=10,
                                validators=[
                                    MinValueValidator(1),
                                    MaxValueValidator(50),
                                ],
                                verbose_name='quantidade',
                                help_text='Número de resultados para retornar na resposta')
    offset = models.IntegerField(default=0,
                                 verbose_name='offset',
                                 help_text='Número de respostas que serão puladas antes de retornar o resultado',
                                 validators=[MinValueValidator(0)])
    mkt = models.CharField(max_length=5,
                           verbose_name='mercado',
                           help_text='Mercado do qual os resultados serão buscados',
                           choices=MktOptions,
                           default=MktOptions.BRAZIL)
    freshness = models.CharField(max_length=5,
                                 verbose_name='mais recentes',
                                 help_text='O quão recente as notícias retornadas devem ser',
                                 choices=FreshnessOptions,
                                 default=FreshnessOptions.DAY)

    created_at = models.DateTimeField(auto_now_add=True, 
                                      verbose_name='criado em')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='atualizado em')
    

    def __str__(self):
        return self.query_term

    

