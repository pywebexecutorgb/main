'use strict';

/**
 * Function enable notification block and show message.
 * @param message: string
 */
function showNotification(message) {
  let notification = document.querySelector('.notification');
  notification.hidden = false;
  notification.textContent = message;
}

/*
 * Initialize container on page load.
 */
window.addEventListener('DOMContentLoaded', () => {
  fetch('/api/containers/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  })
    .then(response => response.json())
    .then((json) => sessionStorage.setItem('containerID', json['container_id']))
    .catch(() => showNotification('Cannot get container ID, please refresh page'))
});

window.addEventListener('unload', () => deleteContainer());

/**
 * Function make DELETE request, that remove container.
 * Successful status code = 204.
 */
function deleteContainer() {
  let containerID = sessionStorage.getItem('containerID');
  if (containerID) {
    fetch(`/api/containers/${containerID}/`, {
      method: 'DELETE',
    })
      .then(() => {
        console.log(`container ${containerID} has deleted`)
      })
      .catch(() => console.log(`Cannot remove container ${containerID}`))
  }
}

window.addEventListener('load', () => sendHealthChecks());

function sendHealthChecks() {
  setInterval(() => {
    let containerID = sessionStorage.getItem('containerID');
    if (!containerID) {
      return False;
    }

    fetch(`/api/containers/${containerID}/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({'date': Date.now()}),
    })
      .then((response) => {
        if (response.status !== 204) {
          throw new Error('received wrong status code');
        }
      })
      .catch(() => showNotification('Error while send container healthcheck, please refresh page'));
  }, 10000);
}