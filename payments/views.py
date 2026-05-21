from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from reservations.models import Reservation
from .models import Payment

from reportlab.pdfgen import canvas

from decimal import Decimal
import random

@login_required
def payment_page(request, reservation_id):

    reservation = get_object_or_404(
        Reservation,
        id=reservation_id,
        user=request.user
    )

    if request.method == "POST":

        payment_type = request.POST.get("payment_type")
        method = request.POST.get("method")
        success = random.choice([True, True, True, True, False])

        try:
            reste = reservation.reste_a_payer()

        except AttributeError:

            total_paye = sum(
                p.amount
                for p in reservation.payments.filter(status='paid')
            )

            reste = (reservation.total or 0) - total_paye
        if reste <= 0:

            return render(
                request,
                "frontend/payments/payment.html",
                {
                    "reservation": reservation,
                    "error": "Ce voyage est déjà entièrement payé ❌"
                }
            )
        if payment_type == "deposit":

            amount = reservation.total * Decimal('0.30')

        else:

            amount = reste

        if amount > reste:
            amount = reste

        amount = Decimal(amount).quantize(
            Decimal("0.01")
        )

        
        if not success:

            Payment.objects.create(
                reservation=reservation,
                amount=amount,
                payment_type=payment_type,
                method=method,
                status='failed'
            )

            return render(
                request,
                "frontend/payments/payment.html",
                {
                    "reservation": reservation,
                    "error": "❌ Paiement refusé, veuillez réessayer"
                }
            )

        Payment.objects.create(
            reservation=reservation,
            amount=amount,
            payment_type=payment_type,
            method=method,
            status='paid'
        )

        
        try:

            reservation.refresh_from_db()

            if reservation.reste_a_payer() <= 0:

                Reservation.objects.filter(
                    id=reservation.id
                ).update(status='confirmed')

            else:

                Reservation.objects.filter(
                    id=reservation.id
                ).update(status='pending')

        except:

            Reservation.objects.filter(
                id=reservation.id
            ).update(status='pending')

        return redirect('payment_success')

    return render(
        request,
        "frontend/payments/payment.html",
        {
            "reservation": reservation
        }
    )


def payment_success(request):

    return render(
        request,
        "frontend/payments/payment_success.html"
    )

def payment_failed(request):

    return render(
        request,
        "frontend/payments/payment_failed.html"
    )

@login_required
def invoice(request, reservation_id):

    reservation = get_object_or_404(
        Reservation,
        id=reservation_id,
        user=request.user
    )

    payments = reservation.payments.all()

    total_paid = (
        reservation.total_paye()
        if hasattr(reservation, 'total_paye')
        else sum(p.amount for p in payments)
    )

    reste = (
        reservation.reste_a_payer()
        if hasattr(reservation, 'reste_a_payer')
        else (reservation.total - total_paid)
    )

    return render(
        request,
        "frontend/payments/invoice.html",
        {
            "reservation": reservation,
            "payments": payments,
            "total_paid": total_paid,
            "reste": reste
        }
    )

@login_required
def invoice_pdf(request, reservation_id):

    reservation = get_object_or_404(
        Reservation,
        id=reservation_id,
        user=request.user
    )

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = (
        f'attachment; '
        f'filename="facture_{reservation.id}.pdf"'
    )

    p = canvas.Canvas(response)

    y = 800

    p.setFont(
        "Helvetica-Bold",
        18
    )

    p.drawString(
        220,
        y,
        "FACTURE"
    )

    y -= 50

    p.setFont(
        "Helvetica",
        12
    )

    total_paye = (
        reservation.total_paye()
        if hasattr(reservation, 'total_paye')
        else 0
    )

    reste = (
        reservation.reste_a_payer()
        if hasattr(reservation, 'reste_a_payer')
        else 0
    )

    infos = [

        f"Reservation ID : {reservation.id}",

        f"Client : {reservation.user.username}",

        f"Voyage : {reservation.voyage.title}",

        f"Destination : {reservation.voyage.destination}",

        f"Date arrivee : {reservation.date_arrivee}",

        f"Date retour : {reservation.date_retour}",

        f"Personnes : {reservation.personnes}",

        f"Montant total : {reservation.total} DH",

        f"Total paye : {total_paye} DH",

        f"Reste : {reste} DH"
    ]

    for info in infos:

        p.drawString(
            50,
            y,
            info
        )

        y -= 30

    
    y -= 20

    p.drawString(
        50,
        y,
        "Merci pour votre confiance ✈️"
    )

    p.showPage()

    p.save()

    return response