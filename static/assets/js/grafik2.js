var ctx2 = document.getElementById('doughnut').getContext('2d');
var myChart2 = new Chart(ctx2, {
    type: 'doughnut',
    data: {
        labels: ['Academic', 'Seni', 'Olahraga'],

        datasets: [{
            label: 'Employees',
            data: [42, 12, 8],
            backgroundColor: [
                'rgba(41, 155, 99, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)'
                

            ],
            borderColor: [
                'rgba(41, 155, 99, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)'
             

            ],
            borderWidth: 1
        }]

    },
    options: {
        responsive: true
    }
});