document.addEventListener('DOMContentLoaded', function() {
    const carList = document.getElementById('car-list');
    const carForm = document.getElementById('car-form');
    const makeInput = document.getElementById('make');
    const modelInput = document.getElementById('model');
    const yearInput = document.getElementById('year');

    // Загрузка автомобилей с API
    function loadCars() {
        fetch('/api/cars', {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка сети: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            carList.innerHTML = '';
            data.forEach(car => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${car.make}</td>
                    <td>${car.model}</td>
                    <td>${car.year}</td>
                    <td>
                        <button class="btn btn-primary edit-car" data-id="${car.id}">Редактировать</button>
                        <button class="btn btn-danger delete-car" data-id="${car.id}">Удалить</button>
                    </td>
                `;
                carList.appendChild(row);
            });
        })
        .catch(error => console.error('Ошибка загрузки автомобилей:', error));
    }

    // Добавление автомобиля
    carForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const newCar = {
            make: makeInput.value,
            model: modelInput.value,
            year: yearInput.value
        };
        fetch('/api/cars', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },
            body: JSON.stringify(newCar)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка сети: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log('Автомобиль добавлен:', data);
            loadCars();
            makeInput.value = '';
            modelInput.value = '';
            yearInput.value = '';
        })
        .catch(error => console.error('Ошибка добавления автомобиля:', error));
    });

    // Редактирование автомобиля
    carList.addEventListener('click', function(event) {
        if (event.target.classList.contains('edit-car')) {
            const carId = event.target.getAttribute('data-id');
            const make = prompt('Введите новую марку:');
            const model = prompt('Введите новую модель:');
            const year = prompt('Введите новый год:');
            if (make && model && year) {
                fetch(`/api/cars/${carId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + localStorage.getItem('token')
                    },
                    body: JSON.stringify({ make, model, year })
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Ошибка сети: ' + response.statusText);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Автомобиль обновлен:', data);
                    loadCars();
                })
                .catch(error => console.error('Ошибка обновления автомобиля:', error));
            }
        }
    });

    // Удаление автомобиля
    carList.addEventListener('click', function(event) {
        if (event.target.classList.contains('delete-car')) {
            const carId = event.target.getAttribute('data-id');
            fetch(`/api/cars/${carId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': 'Bearer ' + localStorage.getItem('token')
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Ошибка сети: ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                console.log('Автомобиль удален:', data);
                loadCars();
            })
            .catch(error => console.error('Ошибка удаления автомобиля:', error));
        }
    });

    // Загрузка автомобилей при загрузке страницы
    loadCars();
});
