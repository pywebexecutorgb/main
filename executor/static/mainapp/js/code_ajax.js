'use strict';

window.addEventListener('load', () => { // после загрузки страницы навешиваем слушатель "клик"
  document.querySelector('#execute_button').addEventListener('click', (event) => {
    event.preventDefault(); // отключаем стандартное действие кнопки
    event.target.dataset.defaultValue = event.target.innerText; // добавляем для кнопки описание по умолчанию

    // если поле с кодом пустое - ничего не делаем
    if (document.querySelector('#id_code_text').value === '') {
      return
    }

    const hReq = new XMLHttpRequest();

    // собираем данные в форме для отправки
    const form = document.querySelector('#code_create_form');
    const data = new FormData(form);


    // отправляем AJAX-запрос
    let urlReq = '/api/code-bases/';
    const containerID = sessionStorage.getItem('containerID');
    if (containerID) {
      urlReq = `/api/containers/${containerID}/codes/`;
    }
    hReq.open('POST', urlReq, true);
    hReq.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    hReq.send(data);

    // меняем текст в кнопке и делаем неактивной, чтобы было понятно, что что-то начало происходить
    event.target.innerText = 'Executing...';
    event.target.disabled = true;
    document.getElementById('loader').hidden = false;


    hReq.onreadystatechange = () => { // при изменении статуса запроса
      if (hReq.readyState === 4) { // если всё вернулось нормально
        // складываем рабочие объекты в переменные для удобства работы
        const outputResult = document.querySelector('#output-result');
        const response = JSON.parse(hReq.response);
        sessionStorage.setItem('latestProfile', response['profile']);
        sessionStorage.setItem('latestOutput', response['output']);

        event.target.innerText = event.target.dataset.defaultValue; // возвращаем исходный текст кнопки из шаблона
        event.target.disabled = false;
        document.getElementById('loader').hidden = true;

        outputResult.value = response['output']; // выводим результат выполнения кода
        outputResult.classList.remove('blinking'); // удаляем эффект мигания курсора

        // если есть профайл, делмаем активной кнопку и выставляем ей значение по умолчанию
        const viewButton = document.getElementById("view-button");
        viewButton.hidden = !response.hasOwnProperty('profile');
        viewButton.textContent = 'Profile';

        if (response['has_errors']) { // если вернулся код с ошибками
          outputResult.classList.add('error-message'); // меняем класс на ошибочный
        } else { // если вернулся код без ошибок
          outputResult.classList.remove('error-message'); // убираем ошибочный класс
        }

        if (!response['code'] || !response['code']['url']) {
          return;
        }

        // обновляем location результата
        let url = document.getElementById('url-result');
        url.dataset.location = response['code']['url'];
        // update address bar
        history.pushState('update URL', '', window.location.origin + url.dataset.location);

      }
    };

  });
});
