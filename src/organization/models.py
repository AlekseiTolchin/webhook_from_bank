from django.db import models


class Organization(models.Model):
    """Модель организации с ИНН и балансом."""
    inn = models.CharField(
        verbose_name='ИНН',
        max_length=12,
        unique=True,
    )
    balance = models.DecimalField(
        verbose_name='Баланс',
        max_digits=20,
        decimal_places=2,
        default=0,
    )

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return f'ИНН {self.inn}'


class Payment(models.Model):
    """Модель банковского платежа."""
    operation_id = models.UUIDField(
        verbose_name='id операции',
        unique=True,
    )
    amount = models.DecimalField(
        verbose_name='Сумма',
        max_digits=20,
        decimal_places=2,
    )
    payer_inn = models.CharField(
        verbose_name='ИНН плательщика',
        max_length=12,
    )
    document_number = models.CharField(
        verbose_name='Номер документа',
        max_length=20,
    )
    document_date = models.DateTimeField(
        verbose_name='Дата документа',
    )
    organization = models.ForeignKey(
        Organization,
        verbose_name='Организация',
        on_delete=models.CASCADE,
        null=True,
        related_name='payments',
    )

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'


class BalanceLog(models.Model):
    """Журнал изменения баланса организации."""
    date = models.DateTimeField(
        verbose_name='Дата',
        auto_now_add=True,
    )
    organization = models.ForeignKey(
        Organization,
        verbose_name='Организация',
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        verbose_name='Поступившая сумма',
        max_digits=20,
        decimal_places=2,
    )
    new_balance = models.DecimalField(
        verbose_name='Обновленный баланс',
        max_digits=20,
        decimal_places=2,
    )

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
