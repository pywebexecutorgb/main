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