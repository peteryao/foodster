from django.contrib import admin
from order.models import Restraunt, Food, Order, Rating
# Register your models here.

class RestrauntAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'description', 'owner', 'longitude', 'latitude', 'modified', 'created']

class FoodAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'description', 'cost', 'portrait_photo', 'modified', 'created']

class OrderAdmin(admin.ModelAdmin):
	list_display = ['id', 'restraunt', 'food', 'amount', 'user', 'transaction_id', 'status', 'modified', 'created']

class RatingAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'restraunt', 'description', 'rating', 'modified', 'created']

admin.site.register(Restraunt, RestrauntAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Rating, RatingAdmin)