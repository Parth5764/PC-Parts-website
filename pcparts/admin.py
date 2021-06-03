from django.contrib import admin
from .models import processor
from .models import ram
from .models import storage
from .models import motherboard
from .models import powersupply
from .models import gpu
from .models import cart
from .models import extendeduser

# Register your models here.

admin.site.register(processor)
admin.site.register(ram)
admin.site.register(storage)
admin.site.register(motherboard)
admin.site.register(powersupply)
admin.site.register(gpu)
admin.site.register(cart)
admin.site.register(extendeduser)