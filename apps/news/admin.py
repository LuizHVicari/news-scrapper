from django.contrib import admin

from .models import Query, News


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ['query_term', 'count', 'offset', 'mkt', 'freshness', 'created_at']
    list_filter = ['count', 'offset', 'mkt', 'freshness', 'created_at', 'updated_at']
    search_fields = ['query_term']
    list_editable = ['count', 'offset', 'mkt', 'freshness']
    ordering = ['-updated_at']
    

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'date_published', 'created_at']
    # list_display_links = ['query']
    ordering = ['-updated_at']