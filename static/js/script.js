document.addEventListener('DOMContentLoaded', function () {

    console.log(monthlyLabels);
    console.log(monthlyData);

    // =========================
    // GRAPHIQUE RÉSERVATIONS
    // =========================

    const ctx1 =
        document.getElementById('monthlyChart');

    if (ctx1 && monthlyLabels.length > 0) {

        new Chart(ctx1, {

            type: 'line',

            data: {

                labels: monthlyLabels,

                datasets: [{

                    label: 'Réservations',

                    data: monthlyData,

                    borderColor: '#c79a2e',

                    backgroundColor:
                        'rgba(199,154,46,0.1)',

                    borderWidth: 3,

                    tension: 0.4,

                    fill: true,

                    pointRadius: 5
                }]
            },

            options: {

                responsive: true
            }
        });
    }

    // =========================
    // DESTINATIONS
    // =========================

    const ctx2 =
        document.getElementById('destinationsChart');

    if (ctx2 && destinationsLabels.length > 0) {

        new Chart(ctx2, {

            type: 'bar',

            data: {

                labels: destinationsLabels,

                datasets: [{

                    label: 'Réservations',

                    data: destinationsData,

                    backgroundColor: '#c79a2e',

                    borderRadius: 10
                }]
            },

            options: {

                responsive: true
            }
        });
    }

});