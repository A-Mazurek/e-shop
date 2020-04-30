from django.contrib import admin
from django.urls import path
from e_shop_app.views import e_shop_day_summary


urlpatterns = [
    path('api/summary/<str:date>', e_shop_day_summary),
    path('admin/', admin.site.urls),
]
