'use strict';

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
    .catch(() => console.log('cannot get Container ID'))
});

window.addEventListener('beforeunload', () => deleteContainer());
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
      .catch(() => console.log(`cannot remove container ${containerID}`))
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
    });
  }, 10000);
}