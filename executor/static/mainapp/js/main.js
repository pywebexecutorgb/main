"use strict";

function resetInputForm(event) {
    document.getElementById('id_code_text').textContent = '';
    document.getElementById('id_dependencies').textContent = '';
}

let btn = document.querySelector('.clear-button');
btn.addEventListener('click', (e) => {
    e.preventDefault();
    resetInputForm(e);
});

let outputResult = document.getElementById('output-result');
if (outputResult.classList.contains('blinking')) {
    setInterval(function () {
        if (outputResult.classList.contains('on')) {
            outputResult.innerHTML = '&#9646;';
            outputResult.classList.remove('on');
        } else {
            outputResult.innerHTML = '&#9647;';
            outputResult.classList.add('on');
        }
    }, 700);
}