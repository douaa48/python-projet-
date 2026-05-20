from django.urls import path

from .views import (
    payment_page,
    payment_success,
    payment_failed,
    invoice,
    invoice_pdf
)

urlpatterns = [

    # 📄 FACTURE HTML
    path(
        'invoice/<int:reservation_id>/',
        invoice,
        name='invoice'
    ),

    # 📄 FACTURE PDF
    path(
        'invoice/pdf/<int:reservation_id>/',
        invoice_pdf,
        name='invoice_pdf'
    ),

    # ✅ SUCCESS
    path( 'success/', payment_success,name='payment_success' ),

    # ❌ FAILED
    path( 'failed/', payment_failed, name='payment_failed'),

    # 💳 PAIEMENT
    path('<int:reservation_id>/',payment_page, name='payment_page'
    ),
]