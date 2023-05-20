from django.contrib import admin

# Register your models here.
from blog.models import Post
# Register your models here.

# admin.site.register(Product)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'slug', 'preview', 'date_of_creation', 'is_published', )
    search_fields = ('header',)
    list_filter = ('is_published',)

