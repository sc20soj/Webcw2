"""paypal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
#from payments.views import createTransaction, getTransaction, getUserTransactions, makePayment, refundTransaction, cancelTransaction
from paystuff.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/createTransaction/', createTransaction),
    path('api/getTransaction', getTransaction),
    path('api/getUserTransactions', getUserTransactions),
    path('api/getEmailTransactions', getUserTransactions),
    path('api/makePayment', makePayment),
    path('api/refundTransaction', refundTransaction),
    path('api/cancelTransaction', cancelTransaction)
]
"""
    path('api/getTransaction/<int:id>', getTransaction),
    path('api/getUserTransactions/<int:id>', getUserTransactions),
    path('api/makePayment/<int:id>', makePayment),
    path('api/refundTransaction/<int:id>', refundTransaction),
    path('api/cancelTransaction/<int:id>', cancelTransaction),
    path('api/deleteTransaction/<int:id>', deleteTransaction)"""