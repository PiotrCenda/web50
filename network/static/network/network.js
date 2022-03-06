document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        document.querySelector('.loader').style.display = 'none';
        document.querySelector('.body').style.display = 'block';
      }, 10);

    document.querySelector('#new-post-form').addEventListener('submit', create_post);
});

function create_post(event) {
  const title = document.querySelector('#new-post-title').value;
  const body = document.querySelector('#new-post-body').value;
  
  if (title === "") {
    alert("Title must not be empty!");
    event.preventDefault();
  } else if (body === "") {
    alert("Post's body must not be empty!");
    event.preventDefault();
  } else {
    return true;
  }
}