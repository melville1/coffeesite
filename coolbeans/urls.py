
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
# line 4 and 5 are needed to create the url for the images

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('beansapp.urls'))

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# LINE 14 CONFIGURES THE STORAGE OF MEDIA, meaning it lets django know where it can find the media


