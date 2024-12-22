function toggleGraph(pointIndex, param) {
    const graphElement = document.getElementById(`graph-${pointIndex}-${param}`);
    if (graphElement.style.display === 'none') {
        graphElement.style.display = 'block';
    } else {
        graphElement.style.display = 'none';
    }
}
