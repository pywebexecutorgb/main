'use strict';

window.onload = () => { // после загрузки страницы навешиваем слушатель "клик"
  document.querySelector('#execute_button').addEventListener('click', (event) => {
    event.preventDefault(); // отключаем стандартное действие кнопки
    
    // если поле с кодом пустое - ничего не делаем
    if (document.querySelector('#id_code_text').value === '') {
      return
    }
    
    const hReq = new XMLHttpRequest();
    
    // собираем данные в форме для отправки
    const form = document.querySelector('#code_create_form');
    const data = new FormData(form);
    // сохраняем изначальный текст кнопки для последующего возврата к этому значнию
    const start_label = event.target.innerText;
    
    // отправляем AJAX-запрос
    hReq.open('POST', '/code/create/', true);
    hReq.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    hReq.send(data);
    
    // меняем текст в кнопке, чтобы было понятно, что что-то начало происходить
    event.target.innerText = 'Executing...';
    
    
    hReq.onreadystatechange = () => { // при изменении статуса запроса
      if (hReq.readyState === 4) { // если всё вернулось нормально
        // складываем рабочие объекты в переменные для удобства работы
        const outputResult = document.querySelector('#output-result');
        const response = JSON.parse(hReq.response);
        
        event.target.innerText = start_label; // возвращаем исходный текст кнопки из шаблона
        outputResult.value = response['output']; // выводим результат выполнения кода
        
        if (response['has_errors']) { // если вернулся код с ошибками
          outputResult.classList.add('error-message'); // меняем класс на ошибочный
        } else { // если вернулся код без ошибок
          outputResult.classList.remove('error-message'); // убираем ошибочный класс
        }
      }
    };
    
  });
}