document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}


// LOAD MAILBOX
function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then((response) => response.json())
  .then((results) => {
    results.forEach((email) => {
      
      if(mailbox == 'inbox'){
        sender = email.recipients;
        if(email.read) isRead = 'border border-dark rounded-lg';
        else isRead = 'border border-primary rounded-lg';
      }else{
        sender = email.sender;
        isRead = 'border border-dark rounded-lg';
      }

      var item = document.createElement('div')
      item.className = `card ${isRead} my-1 items`;
      item.innerHTML = `<div class="card-body" id="item-${email.id}">
                        ${email.subject} | ${sender} | ${email.timestamp}
                        <br>
                        ${email.body.slice(0, 100)}
                        </div>`;
      
      item.addEventListener('click', () => {
        show_email(email.id, mailbox);
      });

      document.querySelector('#emails-view').append(item);
    });
  });
}


// SHOW EMAIL
function show_email(id, mailbox){
  fetch(`/emails/${id}`)
  .then((response) => response.json())
  .then((email) => {
    // Print email
    // console.log(email);
    document.querySelector('#emails-view').innerHTML = "";
    var item = document.createElement('div');
    item.className = 'card';
    item.innerHTML = `<div class="card-body" style="white-space: pre;">
Sender: ${email.sender}
Recipients: ${email.recipients}
Subject: ${email.subject}
Time: ${email.timestamp}
<br>${email.body}
</div>`;
    document.querySelector('#emails-view').appendChild(item);

    if (mailbox == 'sent') return;
    
    let reply = document.createElement('btn');
    reply.className = 'btn btn-primary';
    reply.textContent = 'Reply';
    reply.addEventListener('click', () => {
      reply_mail(email.sender, email.subject, email.body, email.timestamp);
    });
    document.querySelector('#emails-view').appendChild(reply);

    let archive = document.createElement('btn');
    archive.className = 'btn btn-outline-dark';
    if (!email.archived) archive.textContent = 'Archive';
    else archive.textContent = 'Unarchive';
    archive.addEventListener('click', () => {
      archiveMail(id, email.archived);
      if (archive.innerText == 'Archive') archive.innerText = 'Unarchive';
      else archive.innerText = 'Archive';
    });
    document.querySelector('#emails-view').appendChild(archive);

    read(id);
  });
}


// REPLY TO EMAIL
function reply_mail(sender, subject, body, timestamp) {
  compose_email();
  if (!/^Re:/.test(subject)) subject = `Re: ${subject}`;

  document.querySelector("#compose-recipients").value = sender;
  document.querySelector("#compose-subject").value = subject;

  fill = `\n\n\nOn ${timestamp} ${sender} wrote:\n${body}\n`;

  document.querySelector("#compose-body").value = fill;
}


// ARCHIVE OR NOT
function archiveMail(id, state){
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: !state
    })
  });
}


// MAKE READ
function read(id){
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  });
}