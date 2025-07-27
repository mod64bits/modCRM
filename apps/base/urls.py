from django.urls import path, include


urlpatterns = [

    path('users/', include('apps.account.urls')),
    path('empresas/', include('apps.company.urls')),
    path('rondas/', include('apps.mod_ronda.urls')),

]
