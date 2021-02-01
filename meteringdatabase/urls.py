"""meteringdatabase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.urls import path, include
from metering_database import views
from register import views as v
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('success', views.success, name = 'success'),
    path('submission', views.submission, name = 'submission'),
    path('new_submission', views.new_submission, name = 'new_submission'),
    path('welcome', views.welcome, name = 'welcome'),
    path('fillform', views.fillform, name = 'fillform'),
    path('newmeter', views.newmeter, name = 'newmeter'),
    path('querries',views.querries, name = 'querries'),
    path('homepage', views.homepage, name = 'homepage'),
    path('querriesback', views.querriesback, name = 'querriesback'),
    #path('create', v.create, name = 'create'),
    path('meterrecord', views.meterrecord, name = 'meterrecord'),
    path('sub_meterrecord', views.sub_meterrecord, name = 'sub_meterrecord'),
    path('standalone', views.standalone, name = 'standalone'),
    path('substation', views.substation, name = 'substation'),
    path('monthly_LP', views.monthly_LP, name = 'monthly_LP'),
    path('new_LP', views.new_LP, name = 'new_LP'),
    path('LP_plot', views.LP_plot, name = 'LP_plot'),
    path('umeme', views.umeme, name = 'umeme'),
    path('bill_gen', views.bill_gen, name = 'bill_gen'),




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
