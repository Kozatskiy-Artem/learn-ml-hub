document.addEventListener('DOMContentLoaded', function () {
    var data1 = JSON.parse(document.getElementById('accuracy').getAttribute('data-data1'));
    var data2 = JSON.parse(document.getElementById('accuracy').getAttribute('data-data2'));
    var data3 = JSON.parse(document.getElementById('accuracy').getAttribute('data-data3'));

    var ctx = document.getElementById('accuracy').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data3,
            datasets: [
                {
                    label: 'Accuracy',
                    data: data1,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                    fill: false
                },
                {
                    label: 'Val accuracy',
                    data: data2,
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1,
                    fill: false
                }
            ]
        },
        options: {
            scales: {
                x: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Epoch'
                    }
                }],
                y: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Value'
                    }
                }]
            }
        }
    });
});