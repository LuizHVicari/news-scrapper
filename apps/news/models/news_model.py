from django.db import models

from .query_model import Query


class News(models.Model):
    class Meta:
        verbose_name = 'Notícia'
        verbose_name_plural = 'Notícias'

    
    name = models.TextField(verbose_name='título')
    description = models.TextField(verbose_name='descrição')
    url = models.URLField(verbose_name='link', 
                          help_text='Link da notícia',
                          unique=True)
    date_published = models.DateTimeField(verbose_name='data de publicação')

    query = models.ForeignKey(Query, null=True, blank=True, 
                              on_delete=models.CASCADE,
                              verbose_name='busca')

    created_at = models.DateTimeField(auto_now_add=True, 
                                      verbose_name='criado em')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='atualizado em')
    

    def __str__(self):
        return self.name