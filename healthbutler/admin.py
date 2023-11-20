from django.contrib import admin

# Register your models here.
from .models import user
from .models import Profile


# Register your models here.
admin.site.register(user)

from django.contrib import admin
from .models import FoodTypes, Foods

class FoodTypesAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(FoodTypes, FoodTypesAdmin)

class FoodsAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'serving','calories',
                    'fat', 'carbs', 'fiber','protein']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Foods, FoodsAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'weight', 'height']
    raw_id_fields = ['user']
