from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy
from django.db import models
from datetime import datetime

class Instrument(models.Model):

    class Meta:
        db_table = "instruments"
        verbose_name = "Доступный инструмент"
        verbose_name_plural = "Доступные интсрументы"

    manufacturer = models.TextField(verbose_name="Производитель")
    model = models.TextField(verbose_name="Модель")

    def __str__(self):
        return f"{self.manufacturer} {self.model}"

class Customer(models.Model):

    class Meta:
        db_table = "customers"
        verbose_name = "Описание контрагента"
        verbose_name_plural = "Описание контрагентов"

    customer_name = models.TextField(verbose_name="Наименование организации")
    customer_address = models.TextField(verbose_name="Адрес")

    def __str__(self):
        return self.customer_name

class InstrumentInField(models.Model):

    class Meta:
        db_table = "instrument_in_fields"
        verbose_name = "Инструмент в полях"
        verbose_name_plural = "Инструменты в полях"

    serial_number = models.TextField(verbose_name='Серийный номер')
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT, verbose_name="Идентификатор пользователя")
    analyzer = models.ForeignKey(Instrument, on_delete=models.RESTRICT, verbose_name="Идентификатор инструмента")
    owner_status = models.TextField(verbose_name="Статус принадлежности")

    def __str__(self):
        return f"{self.serial_number} {self.analyzer_id}"

def status_validator(order_status):
    if order_status not in ["open", "closed", "in progress", "need info"]:
        raise ValidationError(
            gettext_lazy('%(order_status)s is wrong order status'),
            params={'order_status': order_status},
        )


class Order(models.Model):

    class Meta:
        db_table = "orders"
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    device = models.ForeignKey(InstrumentInField, verbose_name="Инструмент", on_delete=models.RESTRICT)
    customer = models.ForeignKey(Customer, verbose_name="Конечный пользователь", on_delete=models.RESTRICT)
    order_description = models.TextField(verbose_name="Описание")
    created_dt = models.DateTimeField(verbose_name="Создано", auto_now_add=True)
    last_updated_dt = models.DateTimeField(verbose_name="Последнее изменение", blank=True, null=True)
    order_status = models.TextField(verbose_name="Статус заявки", validators=[status_validator])

    def save(self, *args, **kwargs):
        self.last_updated_dt = datetime.now()
        super().save(*args, **kwargs)