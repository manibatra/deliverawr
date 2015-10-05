from django.contrib import admin
from .models import Restaurant, DeliveryLocation, MenuItem, DeliveryHours

# Register your models here.
# class MenuItemAdmin(admin.ModelAdmin):
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == "option":
#             kwargs["queryset"] = MenuItem.objects.filter(restaurant=self.restaurant)
#         return super(MenuItemAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class DeliveryLocationInline(admin.StackedInline):
	model = DeliveryLocation

class MenuItemInline(admin.TabularInline):
    model = MenuItem

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):

        field = super(MenuItemInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == 'option':
            if request._obj_ is not None:
                field.queryset = field.queryset.filter(restaurant__exact = request._obj_, option_category="")
            else:
                field.queryset = field.queryset.none()

        return field

class RestaurantAdmin(admin.ModelAdmin):
    inlines = [
        MenuItemInline,
        DeliveryLocationInline,
    ]

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        return super(RestaurantAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(DeliveryHours)
