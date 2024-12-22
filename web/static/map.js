document.addEventListener('DOMContentLoaded', function () {
    // Получаем список городов из переменной Flask
    const cities = JSON.parse(document.getElementById('cities-data').textContent);  // Получаем данные из элемента

    if (!Array.isArray(cities) || cities.length === 0) {
        console.error("Нет данных о городах для отображения.");
    } else {
        const cityNames = cities.map(city => city['city']);
        const latitudes = cities.map(city => city['latitude']);
        const longitudes = cities.map(city => city['longitude']);

        // Создаем массив данных для карты
        const data = [{
            type: 'scattergeo',
            mode: 'markers',
            text: cityNames,
            lon: longitudes,
            lat: latitudes,
            marker: {
                size: 10,
                color: 'blue',
                symbol: 'circle',
                line: {
                    width: 0.5
                }
            }
        }];

        // Устанавливаем параметры карты
        const layout = {
            title: 'Карта городов',
            geo: {
                scope: 'world',
                showland: true,
                landcolor: 'lightgray',
                subunitcolor: 'gray',
                countrycolor: 'gray'
            }
        };

        // Отображаем карту
        Plotly.newPlot('map', data, layout);
    }
});
