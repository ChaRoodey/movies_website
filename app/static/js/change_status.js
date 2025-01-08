function changeStatus(movieId, status) {
    fetch(`/movie/change_status`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ movie_id: movieId, status: status }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            } else {
                alert('Ошибка при смене статуса');
            }
        })
        .catch(error => console.error('Ошибка:', error));
}
