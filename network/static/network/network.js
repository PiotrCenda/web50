document.addEventListener('DOMContentLoaded', () => {
  document.querySelector('#new-post-form').addEventListener('submit', create_post);

  load(number=1);
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

function load(number) {
  fetch(`/load/${number}`)
  .then(response => response.json())
  .then(page_obj => {
    document.querySelector('#posts').replaceChildren();

    page_obj["posts"].forEach(
      post => createPostElement(post)
    );

    updatePaginatorElement(page_obj["has_next"], page_obj["has_previous"], page_obj["current"]);
  })
  .catch(e => console.log('error: ' + e));
}

function createPostElement(post) {
  const template = document.querySelector('#post-element-template');
  let element = template.content.cloneNode(true);

  element.querySelector("#title").textContent = post["title"];
  element.querySelector("#time").textContent = post["timestamp"];
  element.querySelector("#owner").textContent = post["owner_name"];
  element.querySelector("#text").textContent = post["text"];
  element.querySelector("#likes").textContent = `Likes: ${post["likes"]}`;

  document.querySelector('#posts').appendChild(element);
}

function updatePaginatorElement(next, previous, current) {
  const template = document.querySelector('#pagination-template');
  let pagination = template.content.cloneNode(true).querySelector("#pagination");
  document.querySelector('#pagination').replaceChildren();
  
  pagination.querySelector("#current").textContent = current;

  if (next) {
    pagination.querySelector("#next").addEventListener('click', () => load(number=(current+1)), false);
  } else {
    pagination.querySelector("#next").setAttribute("tabindex", "-1");
    pagination.querySelector("#next").setAttribute("aria-disabled", "true");
  }

  if (previous) {
    pagination.querySelector("#previous").addEventListener('click', () => load(number=(current-1)), false);
  } else {
    pagination.querySelector("#previous").setAttribute("tabindex", "-1");
    pagination.querySelector("#previous").setAttribute("aria-disabled", "true");
  }

  document.querySelector('#pagination').appendChild(pagination)
}