from django.contrib import admin

from .models import Advertisement,Category , Post ,Tag,OurTeam,Contact
# Register your models here.

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Advertisement)
admin.site.register(OurTeam)
admin.site.register(Contact)