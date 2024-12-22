let intermediatePoints = 0;

function addIntermediatePoint() {
    const container = document.getElementById("intermediate-points-container");
    const index = intermediatePoints++;

    // Создаем HTML для новой промежуточной точки с кнопкой для удаления
    const pointHTML = `
        <div id="intermediate-point-${index}" class="intermediate-point">
            <h2>Промежуточная точка ${index + 1}</h2>
            <label for="intermediate_city_${index}">Город:</label>
            <input type="text" name="intermediate_city_${index}" id="intermediate_city_${index}" required>
            <button type="button" onclick="removeIntermediatePoint(${index})">Удалить</button>
        </div>`;

    container.insertAdjacentHTML('beforeend', pointHTML);
    updateIntermediatePointsCount();
}

function removeIntermediatePoint(index) {
    const point = document.getElementById(`intermediate-point-${index}`);
    if (point) {
        point.remove();
        updateIntermediatePointsCount();
    }
}

function updateIntermediatePointsCount() {
    // Обновляем счетчик количества промежуточных точек
    const container = document.getElementById("intermediate-points-container");
    const points = container.getElementsByClassName("intermediate-point");
    document.getElementById("num_intermediate_points").value = points.length;
}
