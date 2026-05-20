from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now

from voyages.models import Voyage

from .forms import ReservationForm
from .models import Reservation


@login_required
def reservation_list(request):
    reservations = (
        Reservation.objects
        .filter(user=request.user)
        .select_related("voyage")
        .prefetch_related("options", "payments")
        .order_by("-created_at")
    )

    return render(request, "frontend/reservations/reservation_list.html", {
        "reservations": reservations
    })


@login_required
def reservation_form(request, id):
    voyage = get_object_or_404(Voyage, id=id, is_active=True)

    if request.method == "POST":
        form = ReservationForm(request.POST, voyage=voyage)

        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.voyage = voyage
            reservation.total = form.montant_total()
            reservation.status = "pending"
            reservation.save()
            form.save_m2m()

            messages.success(request, "Reservation creee avec succes.")
            return redirect("payment_page", reservation_id=reservation.id)

        messages.error(request, "Merci de corriger les erreurs du formulaire.")
    else:
        form = ReservationForm(voyage=voyage)

    return render(request, "frontend/reservations/reservation_form.html", {
        "voyage": voyage,
        "form": form,
        "places_restantes": voyage.places_restantes(),
    })


@login_required
def cancel_reservation(request, id):
    reservation = get_object_or_404(
        Reservation.objects.select_related("voyage").prefetch_related("payments"),
        id=id,
        user=request.user,
    )

    if reservation.status == "cancelled":
        messages.error(request, "Reservation deja annulee.")
        return redirect("reservation_list")

    if not reservation.date_arrivee:
        messages.error(request, "Erreur sur la reservation.")
        return redirect("reservation_list")

    days_before = (reservation.date_arrivee - now().date()).days

    if days_before < 3:
        messages.error(request, "Annulation refusee: moins de 3 jours avant le depart.")
        return redirect("reservation_list")

    payments = reservation.payments.filter(status="paid")
    total_paid = sum(payment.amount for payment in payments)
    remboursement = Decimal("0.00")

    if days_before >= 7:
        remboursement = total_paid
    elif days_before >= 3:
        remboursement = total_paid * Decimal("0.50")

    if remboursement > 0:
        payments.update(status="refunded")

    reservation.status = "cancelled"
    reservation.save()

    messages.success(
        request,
        f"Reservation annulee. Remboursement simule: {remboursement:.2f} DH",
    )

    return redirect("reservation_list")
