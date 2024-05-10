// script.js
document.addEventListener("DOMContentLoaded", function () {
    // Создаем карту, указываем координаты центра и начальный масштаб
    var map = L.map('map').setView([60, 0], 1);
    
    // Добавляем локальные тайлы
    L.tileLayer('tiles/{z}/{x}/{y}.jpg', {
        minZoom: 3, // Минимальный зум
        maxZoom: 6, // Максимальный зум
        tileSize: 256,
        attribution: '&copy; OpenStreetMap contributors',
        noWrap: true
    }).addTo(map);

    // Пример добавления маркера с текстом
    var marker = L.marker([6, 0]).addTo(map)
        .bindPopup('Начальный маркер')
        .openPopup();

    // Определяем иконку для нового маркера
    var suboyIcon = L.icon({
        iconUrl: 'suboy.png', // Путь к изображению иконки
        iconSize: [50, 50],  // Размеры иконки
        iconAnchor: [25, 50], // Точка, которая будет соответствовать координатам маркера
        popupAnchor: [0, -50] // Точка, откуда будет "выпадать" всплывающее окно
    });

    // Добавляем маркер с иконкой suboy.png
    var imageMarker = L.marker([20, 140], {icon: suboyIcon}).addTo(map)
        .bindPopup('О, С ПАСХОЙ!🎉');

    // Добавляем элемент для отображения текущего масштаба
    var zoomDisplay = L.control({position: 'bottomleft'});
    zoomDisplay.onAdd = function (map) {
        var div = L.DomUtil.create('div', 'zoom-display');
        div.innerHTML = 'Масштаб: ' + map.getZoom();
        return div;
    };
    zoomDisplay.addTo(map);

    // Обновляем отображение масштаба при изменении масштаба карты
    map.on('zoomend', function () {
        document.querySelector('.zoom-display').innerHTML = 'Масштаб: ' + map.getZoom();
    });
});