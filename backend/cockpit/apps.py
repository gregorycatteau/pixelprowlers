from django.apps import AppConfig


class CockpitConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cockpit"
    verbose_name = "Cockpit"

    def ready(self):
        from django.contrib import admin

        admin.site.index_template = "admin/index.html"
        admin.site.site_header = "PixelProwlers · Administration"
        admin.site.site_title = "PixelProwlers Cockpit"
        admin.site.index_title = "Vue opérationnelle"
