from django.shortcuts import render
from django.db.models import Q, Count
from django.db.models.functions import TruncMonth
from django.contrib.admin.views.decorators import staff_member_required

from voyages.models import Voyage
from reservations.models import Reservation
from users.models import User

import json


@staff_member_required
def admin_dashboard(request):

    # =========================
    # RECHERCHE
    # =========================

    query = request.GET.get('q')

    # =========================
    # STATISTIQUES
    # =========================

    total_voyages = Voyage.objects.count()

    total_reservations = Reservation.objects.count()

    total_clients = User.objects.count()

    revenus = sum(
        r.total or 0
        for r in Reservation.objects.filter(
            status='confirmed'
        )
    )

    # =========================
    # RÉSERVATIONS RÉCENTES
    # =========================

    if query:

        reservations_recentes = (

            Reservation.objects.filter(

                Q(
                    voyage__title__icontains=query
                ) |

                Q(
                    user__username__icontains=query
                )

            ).order_by('-created_at')[:5]
        )

    else:

        reservations_recentes = (

            Reservation.objects.order_by(
                '-created_at'
            )[:5]
        )

    # =========================
    # VOYAGES POPULAIRES
    # =========================

    voyages_populaires = Voyage.objects.all()[:5]

    # =========================
    # GRAPHIQUE MENSUEL
    # =========================

    reservations_par_mois = (

        Reservation.objects

        .annotate(
            month=TruncMonth('created_at')
        )

        .values('month')

        .annotate(
            total=Count('id')
        )

        .order_by('month')
    )

    monthly_labels = []

    monthly_data = []

    for item in reservations_par_mois:

        if item['month']:

            monthly_labels.append(
                item['month'].strftime('%b')
            )

            monthly_data.append(
                item['total']
            )

    # =========================
    # TOP DESTINATIONS
    # =========================

    destinations_labels = []

    destinations_data = []

    for voyage in voyages_populaires:

        destinations_labels.append(
            voyage.destination
        )

        destinations_data.append(

            Reservation.objects.filter(
                voyage=voyage
            ).count()
        )

    # =========================
    # CONTEXT
    # =========================

    context = {

        'total_voyages':
            total_voyages,

        'total_reservations':
            total_reservations,

        'total_clients':
            total_clients,

        'revenus':
            revenus,

        'reservations_recentes':
            reservations_recentes,

        'voyages_populaires':
            voyages_populaires,

        'monthly_labels':
            json.dumps(monthly_labels),

        'monthly_data':
            json.dumps(monthly_data),

        'destinations_labels':
            json.dumps(destinations_labels),

        'destinations_data':
            json.dumps(destinations_data),
    }

    return render(

        request,

        'frontend/dashboard/admin_dashboard.html',

        context
    )