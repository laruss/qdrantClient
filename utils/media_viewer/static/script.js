document.addEventListener('DOMContentLoaded', function() {
    const mediaPathInput = document.getElementById('mediaPath');
    const pathForm = document.getElementById('pathForm');
    const imageElement1 = document.getElementById('image1');
    const imageElement2 = document.getElementById('image2');
    const modeButton = document.getElementById('modeButton');
    let currentImageElement = imageElement1;
    let nextImageElement = imageElement2;

    // Обработка формы установки пути
    if (pathForm) {
        pathForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const mediaPath = mediaPathInput.value;
            fetch('/set_media_path', {
                method: 'POST',
                body: new FormData(pathForm)
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    localStorage.setItem('mediaPath', mediaPath);
                    window.location.href = '/viewer';
                }
            });
        });
    }

    // Функциональность просмотра изображений
    if (currentImageElement && nextImageElement) {
        function loadImage() {
            fetch('/get_image')
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        alert(data.error);
                    } else {
                        currentImageElement.src = data.image_url;
                        currentImageElement.classList.add('active');
                    }
                });
        }

        loadImage();

        document.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowRight') {
                fetch('/next_image', { method: 'POST' })
                    .then(() => {
                        slideImage('left');
                    });
            } else if (e.key === 'ArrowLeft') {
                fetch('/prev_image', { method: 'POST' })
                    .then(() => {
                        slideImage('right');
                    });
            }
        });

        modeButton.addEventListener('click', function() {
            fetch('/change_mode', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    alert('Режим переключен на: ' + data.mode);
                });
        });

        function slideImage(direction) {
            // Убираем классы анимации
            nextImageElement.className = 'image';
            currentImageElement.className = 'image';

            fetch('/get_image')
                .then(response => response.json())
                .then(data => {
                    nextImageElement.src = data.image_url;

                    // Начальное положение следующего изображения
                    if (direction === 'left') {
                        nextImageElement.classList.add('slide-in-right');
                    } else {
                        nextImageElement.classList.add('slide-in-left');
                    }

                    // Переключаем классы для анимации
                    requestAnimationFrame(() => {
                        currentImageElement.classList.add('active');
                        nextImageElement.classList.add('active');

                        if (direction === 'left') {
                            currentImageElement.classList.add('slide-out-left');
                            nextImageElement.classList.remove('slide-in-right');
                        } else {
                            currentImageElement.classList.add('slide-out-right');
                            nextImageElement.classList.remove('slide-in-left');
                        }
                    });

                    // После завершения анимации меняем местами элементы
                    setTimeout(() => {
                        currentImageElement.className = 'image';
                        nextImageElement.className = 'image active';

                        [currentImageElement, nextImageElement] = [nextImageElement, currentImageElement];
                    }, 500); // Время должно совпадать с длительностью transition в CSS
                });
        }
    }
});
