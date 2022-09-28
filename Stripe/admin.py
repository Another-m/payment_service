from django.contrib import admin

from Stripe.models import Item, Order, ItemOrder


class ItemOrderInline(admin.TabularInline):
    model = ItemOrder
    extra = 1


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'price', 'currency', ]
    list_display_links = ['name', 'description']
    list_filter = ['name', 'price']
    list_editable = ['price', 'currency', ]




@admin.register(Order)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', ]
    inlines = [ItemOrderInline]
