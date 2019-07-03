'use strict';

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

window.addEventListener('unload', () => {
  let containerID = sessionStorage.getItem('containerID');
  if (containerID) {
    fetch(`/api/containers/${containerID}`, {
      method: 'DELETE',
    })
      .then(() => {
        console.log(`container ${containerID} has deleted`)
      })
      .catch(() => console.log(`cannot remove container ${containerID}`))
  }
});
