from django.contrib import admin
from mp_churrascos.models import MpTopic, MpEntry, MpUsuarioChurrasco

# Register your models here.
admin.site.register(MpTopic)
admin.site.register(MpEntry)
admin.site.register(MpUsuarioChurrasco)