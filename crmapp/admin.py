from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Lead)
admin.site.register(EmailGroup)
admin.site.register(EmailGroupMember)
admin.site.register(EmailHistory)
