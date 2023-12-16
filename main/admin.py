from django.contrib import admin
from .models import Users, Whishlist, Whishlist_item, Settings
from django.contrib.auth.models import Group, User


admin.site.register(Users)
admin.site.register(Whishlist)
admin.site.register(Whishlist_item)
admin.site.register(Settings)



admin.site.unregister(Group)
admin.site.unregister(User)

admin.site.site_header = "Бот ВИШ. Административная панель"