from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from api.views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'backend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', login_user),
    url(r'^profile/(\w+)', profile),
    url(r'^logout/', logoutPage, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
