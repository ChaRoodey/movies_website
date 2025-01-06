document.addEventListener('DOMContentLoaded', () => {
    const movieSearchForm = document.getElementById('movieSearchForm');
    const movieSearchInput = document.getElementById('movieSearchInput');
    const movieSearchResults = document.getElementById('movieSearchResult');
    const modal = document.getElementById('modal');

    movieSearchForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const title = movieSearchInput.value;
        if (!title) {
            movieSearchResults.innerHTML = '<li class="list-group-item text-danger">Название не может быть пустым!</li>';
            return;
        }

        movieSearchResults.innerHTML = '';

        try {
            const response = await fetch(`/movie/search?title=${encodeURIComponent(title)}`);
            if (!response.ok) {
                throw new Error('Ошибка при поиске фильмов');
            }

            const movies = await response.json();
            console.log('Ответ от сервера: ', movies);

            if (Array.isArray(movies)) {
                movieSearchResults.innerHTML = '';
                movies.forEach(movie => {
                    const listItem = document.createElement('li');
                    listItem.className = 'list-group-item';

                    const movieInfo = document.createElement('div');
                    movieInfo.className = 'movie-info';

                    const posterContainer = document.createElement('div');
                    posterContainer.style.position = 'relative';
                    posterContainer.style.width = '50px';
                    posterContainer.style.height = '75px';

                    const spinner = document.createElement('div');
                    spinner.className = 'spinner-grow text-light';
                    spinner.style.position = 'absolute';
                    spinner.style.top = '50%';
                    spinner.style.left = '50%';
                    spinner.style.transform = 'translate(-50%, -50%)';
                    spinner.style.display = 'block';
                    spinner.style.width = '3rem';
                    spinner.style.height = '3rem';
                    posterContainer.appendChild(spinner);

                    const poster = document.createElement('img');
                    poster.src = movie.poster?.previewUrl || 'default-image.jpg';
                    poster.alt = movie.name || movie.title;
                    poster.style.width = '50px';
                    poster.style.height = '75px';
                    poster.style.objectFit = 'cover';
                    poster.style.display = 'none';

                    poster.onload = function () {
                        spinner.style.display = 'none';
                        poster.style.display = 'block';
                    };

                    posterContainer.appendChild(poster);
                    movieInfo.appendChild(posterContainer);

                    const title = document.createElement('span');
                    title.textContent = movie.name || movie.title || 'Название не указано';
                    title.className = 'movie-title';
                    movieInfo.appendChild(title);

                    const year = document.createElement('span');
                    year.textContent = ` (${movie.year || 'Год не указан'})`;
                    year.className = 'movie-year';
                    movieInfo.appendChild(year);

                    const genre = document.createElement('span');
                    genre.textContent = ` - ${movie.type || 'Категория не указана'}`;
                    genre.className = 'movie-genre';
                    movieInfo.appendChild(genre);

                    const addButton = document.createElement('button');
                    addButton.className = 'btn btn-sm btn-outline-success ml-3';
                    addButton.textContent = 'Добавить к себе';
                    addButton.onclick = () => addMovieToUser(movie.id);
                    movieInfo.appendChild(addButton);

                    listItem.appendChild(movieInfo);
                    movieSearchResults.appendChild(listItem);
                });
            } else {
                movieSearchResults.innerHTML = '<li class="list-group-item text-danger">Некорректный ответ от сервера</li>';
            }


        } catch (error) {
            console.error(error);
            movieSearchResults.innerHTML = '<li class="list-group-item text-danger">Произошла ошибка при поиске</li>';
        }
    });

    async function addMovieToUser(movieId) {
        try {
            const response = await fetch(`/movie/add?movie_id=${movieId}`, {method: 'POST'});
            if (!response.ok) {
                throw new Error('Ошибка при добавлении фильма');
            }

            alert('Фильм добавлен!')
        } catch (error) {
            console.error(error)
            alert('Ошибка при добавлении фильма')
        }
    }

    modal.addEventListener('hidden.bs.modal', () => {
        location.reload();
    });

});

