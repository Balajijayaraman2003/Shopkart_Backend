"""
URL configuration for Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from Auth import urls as Auth_url
from App import urls as App_url
from Orders import urls as Orders_url
from Payments import urls as Payment_url
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/',include(Auth_url)),
    path('app/',include(App_url)),
    path('order/',include(Orders_url)),
    path("payment/",include(Payment_url)),
    ]

from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
