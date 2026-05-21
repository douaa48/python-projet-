from django.urls import path

from .views import (
    payment_page,
    payment_success,
    payment_failed,
    invoice,
    invoice_pdf
)

urlpatterns = [
    path('invoice/<int:reservation_id>/',invoice,name='invoice'),
    path('invoice/pdf/<int:reservation_id>/',invoice_pdf,name='invoice_pdf'),
    path( 'success/', payment_success,name='payment_success' ),
    path( 'failed/', payment_failed, name='payment_failed'),
    path('<int:reservation_id>/',payment_page, name='payment_page'
    ),
]