# import debug_toolbar
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path('basket/', include('core.apps.basket.urls', namespace='basket')),
    path('checkout/', include('core.apps.checkout.urls', namespace='checkout')),
    path('orders/', include('core.apps.orders.urls', namespace='orders')),
    path('', include('core.apps.catalogue.urls', namespace='catalogue')),
    path('account/', include('core.apps.account.urls', namespace='account')),
    # path('__debug__/', include(debug_toolbar.urls)),
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
