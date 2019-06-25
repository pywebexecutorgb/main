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
setInterval(function () {
    if (!outputResult.classList.contains('blinking')) {
        return;
    }

    if (outputResult.classList.contains('on')) {
        outputResult.textContent = null;
        outputResult.classList.remove('on');
    } else {
        outputResult.textContent = '>';
        outputResult.classList.add('on');
    }
}, 1000);
