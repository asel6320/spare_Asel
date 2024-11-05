const ordersLabels = JSON.parse(document.getElementById('ordersChart').dataset.labels);
const ordersData = JSON.parse(document.getElementById('ordersChart').dataset.data);
const ordersCtx = document.getElementById('ordersChart').getContext('2d');
new Chart(ordersCtx, {
    type: 'line',
    data: {
        labels: ordersLabels,
        datasets: [{
            label: 'Заказы',
            data: ordersData,
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            fill: true,
            tension: 0.1
        }]
    }
});

// График новых пользователей
const newUsersLabels = JSON.parse(document.getElementById('newUsersChart').dataset.labels);
const newUsersData = JSON.parse(document.getElementById('newUsersChart').dataset.data);
const newUsersCtx = document.getElementById('newUsersChart').getContext('2d');
new Chart(newUsersCtx, {
    type: 'line',
    data: {
        labels: newUsersLabels,
        datasets: [{
            label: 'Новые пользователи',
            data: newUsersData,
            borderColor: 'rgba(54, 162, 235, 1)',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            fill: true,
            tension: 0.1
        }]
    }
});