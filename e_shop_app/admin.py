from django.contrib import admin
from e_shop_app.models import Product, Promotion, ProductPromotion, Vendor, Customer, Commission, OrderLine, Order


class ProductsAdmin(admin.ModelAdmin):
    search_fields = ['id', 'description']
    list_display = ('id', 'description')


admin.site.register(Product, ProductsAdmin)
admin.site.register(Promotion)
admin.site.register(ProductPromotion)
admin.site.register(Vendor)
admin.site.register(Customer)
admin.site.register(Commission)
admin.site.register(OrderLine)
admin.site.register(Order)
