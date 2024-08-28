from django.db import models


class TelegramUser(models.Model):
    class Meta:
        verbose_name = 'Usuário do Telegram'
        verbose_name_plural = 'Usuários do Telegram'

    first_name = models.CharField(max_length=100, verbose_name='Primeiro Nome')
    telegram_id = models.CharField(max_length=12, unique=True)


    created_at = models.DateTimeField(auto_now_add=True, 
                                    verbose_name='criado em')
    updated_at = models.DateTimeField(auto_now=True,
                                    verbose_name='atualizado em')
    
    def __str__(self):
        return self.telegram_id