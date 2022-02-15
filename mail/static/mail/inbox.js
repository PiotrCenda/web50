document.addEventListener('DOMContentLoaded', function() {

// Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email());
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(prefill = "") {

  console.log(prefill)
  console.log(typeof prefill)

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#detail-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = (prefill) ? prefill["recipient"] : "";
  document.querySelector('#compose-subject').value = (prefill) ? prefill["subject"] : "";
  document.querySelector('#compose-body').value = (prefill) ? prefill["body"] : "";
}

function send_email(event) {
  // Modifies the default beheavor so it doesn't reload the page after submitting.
  event.preventDefault();

  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  if (recipients === "") {
    alert("At least one recipient must be given!");
  } else if (body === "") {
    alert("Email body must not be empty!");
  } else {  
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
    })
    .then(response => response.json())
    .then(() => load_mailbox('sent'))
    .catch(e => console.log('error: ' + e));
  }
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#detail-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {emails.forEach(
    email => createEmailElement(email, mailbox))
  })
  .catch(e => console.log('error: ' + e));
}

function createEmailElement(email, mailbox) {

  const template = document.querySelector('#email-element-template');
  let element = template.content.cloneNode(true);

  element.querySelector("#subject").textContent = (email["subject"].length > 40) ? (email["subject"].slice(0, 40) + "...") : email["subject"];
  element.querySelector("#time").textContent = email["timestamp"];
  element.querySelector("#sender").textContent = email["sender"];
  element.querySelector("#body-preview").textContent = (email["body"].length > 50) ? (email["body"].slice(0, 50) + "...") : email["body"];

  if (email["read"]) {
    element.querySelector("div").style.backgroundColor = "#eeeeee";
  }

  element.querySelector("div").addEventListener('click', () => see_email(email["id"], mailbox))
  document.querySelector('#emails-view').appendChild(element);
}

function see_email(id, mailbox) {
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => createDetailView(email, mailbox))
  .catch(e => console.log('error: ' + e));

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#detail-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })})
    .catch(e => console.log("error: " + e));
}

function createDetailView(email, mailbox) {
  let element = document.querySelector('#detail-view');

  element.querySelector("#subject").innerText = email["subject"];
  element.querySelector("#time").innerText = email["timestamp"];
  element.querySelector("#sender").innerText = email["sender"];
  element.querySelector("#recipients").innerText = email["recipients"].join(", ");
  element.querySelector("#body").innerText = email["body"];

  let archive_button = element.querySelector("#archive")

  if (mailbox !== "sent") {
    archive_button.style.display = 'block';
    archive_button.innerText = (email.archived) ? "Unarchive" : "Archive";
    archive_button.onclick = () => archive_email(email["id"], email["archived"]);
  } else {
    archive_button.style.display = 'none';
  }
  
  element.querySelector("#reply").onclick = () => reply_email(email["id"]);
}

function archive_email(id, archived) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: !archived
    })})
    .catch(e => console.log("error: " + e));

  setTimeout(() => load_mailbox('inbox'), 10);
}

function reply_email(id) {
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    let subject = email.subject;
    let body = email.body;
    
    if (subject.substring(0, 3).toLowerCase() !== "re:") {
      subject = "Re: " + subject;
    }

    body = "On " + email.timestamp + " " + email.sender + " wrote: \n\n" + body;

    prefill = {
      recipient: email.sender,
      subject: subject,
      body: body
    }

    compose_email(prefill);
  })
  .catch(e => console.log('error: ' + e));
}