from django.contrib import admin

from django.contrib import admin

from .models import Order, Instrument, Customer, InstrumentInField


class InstrumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'manufacturer', 'model')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'device', 'customer', 'order_description', 'created_dt', 'last_updated_dt', 'order_status')


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_address')


class InstrumentInFieldAdmin(admin.ModelAdmin):
    list_display = ('id', 'serial_number', 'customer_id', 'analyzer_id', 'owner_status')


admin.site.register(Order, OrderAdmin)
admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(InstrumentInField, InstrumentInFieldAdmin)
