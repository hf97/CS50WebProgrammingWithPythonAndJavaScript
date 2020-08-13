document.addEventListener("DOMContentLoaded", 
  function(){
    const form = document.querySelector("#compose-form");
    const msg = document.querySelector("#message");
    
    form.addEventListener('submit', (event) => {
    
      event.preventDefault();

      fetch("/emails", {
        method: "POST",
        body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value
        }),
      })
      .then((response) => response.json())
      .then((results) => {
        if(results.message === "Email sent successfully."){
          load_mailbox("sent")
        }else{
          msg.innerHTML = `<div class="alert alert-danger" role="alert">${results.error}</div>`;
        }
      });
    });
  },
  false
)
