from django.contrib import admin
from .models import Link,Contact,Privacy,Return,Terms, About

admin.site.register(Link)
admin.site.register(Contact)
admin.site.register(Privacy)
admin.site.register(Return)
admin.site.register(Terms)
admin.site.register(About)