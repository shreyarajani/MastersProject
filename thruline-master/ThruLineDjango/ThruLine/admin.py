from ThruLine.models import *
from django.contrib import admin


class SeasonAdmin(admin.ModelAdmin):
    pass


class EpisodeAdmin(admin.ModelAdmin):
    pass


class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'result_path', 'request')
    pass

admin.site.register(Request, RequestAdmin)
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(Season, SeasonAdmin)
