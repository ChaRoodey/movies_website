document.addEventListener('DOMContentLoaded', () => {
    const movieSearchForm = document.getElementById('movieSearchForm');
    const movieSearchInput = document.getElementById('movieSearchInput');
    const movieSearchResults = document.getElementById('movieSearchResult');

    movieSearchForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const title = movieSearchInput.value;
        if (!title) {
            movieSearchResults.innerHTML = '<li class="list-group-item text-danger">Название не может быть пустым!</li>';
            return;
        } else {
            // alert(`Название фильма: "${title}"`)
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
                    // Создаем новый элемент списка
                    const listItem = document.createElement('li');
                    listItem.className = 'list-group-item';

                    // Создаем контейнер для данных
                    const movieInfo = document.createElement('div');
                    movieInfo.className = 'movie-info';

                    // Добавляем постер
                    // const poster = document.createElement('img');
                    // poster.src = movie.poster?.previewUrl || 'default-image.jpg';
                    // poster.alt = movie.name || movie.title;
                    // poster.style.width = '50px';
                    // poster.style.marginRight = '10px';
                    // movieInfo.appendChild(poster);

                    // Добавляем название
                    const title = document.createElement('span');
                    title.textContent = movie.name || movie.title || 'Название не указано';
                    title.className = 'movie-title';
                    movieInfo.appendChild(title);

                    // Добавляем год выпуска
                    const year = document.createElement('span');
                    year.textContent = ` (${movie.year || 'Год не указан'})`;
                    year.className = 'movie-year';
                    movieInfo.appendChild(year);

                    // Добавляем категорию (тип фильма)
                    const genre = document.createElement('span');
                    genre.textContent = ` - ${movie.type || 'Категория не указана'}`;
                    genre.className = 'movie-genre';
                    movieInfo.appendChild(genre);

                    // Вставляем информацию о фильме в элемент списка
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
});

