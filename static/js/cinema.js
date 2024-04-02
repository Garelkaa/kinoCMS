document.addEventListener('DOMContentLoaded', function() {
    var addButton = document.querySelector('.add_cinema');

    addButton.addEventListener('click', function() {
        var container = document.querySelector('.row.justify-content-center');

        var card = document.createElement('div');
        card.classList.add('card');
        card.style.width = '18rem';

        card.innerHTML = `
            <input type="file" class="form-control photo-input" accept="image/*">
            <div class="card-body">
                <img src="" class="card-img-top" alt="...">
                <input type="text" aria-label="Введите текст..." class="form-control" placeholder="Введите текст...">
                <button class="btn btn-success" style="width: 100%;">Добавить</button>
            </div>
        `;

        container.appendChild(card);

        card.querySelector('.photo-input').addEventListener('change', function(event) {
            var file = event.target.files[0];
            if (file) {
                var reader = new FileReader();
                reader.onload = function() {
                    card.querySelector('.card-img-top').src = reader.result;
                }
                reader.readAsDataURL(file);
            }
        });
    });
});
