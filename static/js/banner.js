document.addEventListener('DOMContentLoaded', function() {
    let addButtonStart = document.querySelector('.add_photo');
    let container = document.getElementById('cardContainer');

    addButtonStart.addEventListener('click', function() {
        let card = document.createElement('div');
        card.classList.add('card');

        card.innerHTML = `
            <input type="file" class="form-control photo-input" accept="image/*">
            <div class="card-body">
                <img src="" class="card-img-top" alt="...">
                <input type="text" aria-label="Ссылка" class="form-control url-input" placeholder="Ссылка">
                <input type="text" aria-label="Введите текст..." class="form-control text-input" placeholder="Введите текст...">
                <button class="btn btn-danger delete-btn" style="width: 100%;">Удалить</button>
            </div>
        `;
        container.appendChild(card);

        card.querySelector('.photo-input').addEventListener('change', function(event) {
            let file = event.target.files[0];
            if (file) {
                let reader = new FileReader();
                reader.onload = function() {
                    card.querySelector('.card-img-top').src = reader.result;
                }
                reader.readAsDataURL(file);
            }
        });

        let deleteButton = card.querySelector('.delete-btn');
        deleteButton.addEventListener('click', function() {
            card.remove(); // Удаляем карточку при нажатии кнопки "Удалить"
        });
    });

    document.getElementById('submitForm').addEventListener('click', function() {
        let cards = document.querySelectorAll('.card');
        let data = [];

        cards.forEach(function(card) {
            let photoInput = card.querySelector('.photo-input');
            let urlInput = card.querySelector('.url-input');
            let textInput = card.querySelector('.text-input');

            let formData = new FormData();
            formData.append('image', photoInput.files[0]);
            formData.append('url', urlInput.value);
            formData.append('text', textInput.value);

            data.push(formData);
        });

        fetch('/url-для-обработки-формы/', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                // Обработка успешной отправки формы
                console.log('Форма успешно отправлена!');
            } else {
                // Обработка ошибки при отправке формы
                console.error('Ошибка при отправке формы');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
    });

    let addButtonEnd = document.querySelector('.add_photo_end');
    addButtonEnd.addEventListener('click', function() {
        let container = document.getElementById('cardContainerEnd');

        let card = document.createElement('div');
        card.classList.add('card');

        card.innerHTML = `
            <input type="file" class="form-control photo-input" accept="image/*">
            <div class="card-body">
                <img src="" class="card-img-top" alt="...">
                <input type="text" aria-label="Ссылка" class="form-control" placeholder="Ссылка">
                <input type="text" aria-label="Введите текст..." class="form-control" placeholder="Введите текст...">
                <button class="btn btn-success" style="width: 100%;">Добавить</button>
                <button class="btn btn-danger delete-btn" style="width: 100%;">Удалить</button>
            </div>
        `;
        container.appendChild(card);

        // Обработчик события для выбора файла
        card.querySelector('.photo-input').addEventListener('change', function(event) {
            let file = event.target.files[0];
            if (file) {
                let reader = new FileReader();
                reader.onload = function() {
                    card.querySelector('.card-img-top').src = reader.result;
                }
                reader.readAsDataURL(file);
            }
        });

        let deleteButton = card.querySelector('.delete-btn');
        deleteButton.addEventListener('click', function() {
            card.remove(); // Удаляем карточку при нажатии кнопки "Удалить"
        });
    });

});
