like = document.querySelectorAll(".liked");

edit = document.querySelectorAll(".edit");
text_area = document.querySelectorAll(".textarea");

like.forEach((element) => {
  like_handeler(element);
});

edit.forEach((element) => {
  element.addEventListener("click", () => {
    edit_handeler(element);
  });
});

text_area.forEach((element) => {
  element.addEventListener("keyup", (e) => {
    // enter e shift faz \n
    if (e.keyCode == 13 && e.shiftKey) return;
    // enter faz save
    if (e.keyCode === 13) edit_handeler(element);
  });
});

function editpost(id, post) {
  form = new FormData();
  form.append("id", id);
  form.append("post", post.trim());
  fetch("/editpost/", {
    method: "POST",
    body: form,
  })
  .then((results) => {
    document.querySelector(`#post-content-${id}`).textContent = post;
    document.querySelector(`#post-content-${id}`).style.display = "block";
    document.querySelector(`#post-edit-${id}`).style.display = "none";
    document.querySelector(`#post-edit-${id}`).value = post.trim();
  });
}

function edit_handeler(element) {
  id = element.getAttribute("data-id");
  edit_btn = document.querySelector(`#edit-btn-${id}`);
  if (edit_btn.textContent == "Edit") {
    document.querySelector(`#post-content-${id}`).style.display = "none";
    document.querySelector(`#post-edit-${id}`).style.display = "block";
    edit_btn.textContent = "Save";
    edit_btn.setAttribute("class", "text-primary edit");
  } else if (edit_btn.textContent == "Save") {
    editpost(id, document.querySelector(`#post-edit-${id}`).value);
    edit_btn.textContent = "Edit";
    edit_btn.setAttribute("class", "text-primary edit");
    time = document.querySelector('mx-2 text-secondary').value
  }
}

function like_handeler(element) {
  element.addEventListener("click", () => {
    id = element.getAttribute("data-id");
    is_liked = element.getAttribute("data-is_liked");
    icon = document.querySelector(`#post-like-${id}`);
    count = document.querySelector(`#post-count-${id}`);

    form = new FormData();
    form.append("id", id);
    form.append("is_liked", is_liked);

    fetch("/like/", {
      method: "POST",
      body: form,
    })
    .then((response) => response.json())
    .then((results) => {
      if (results.status == 201) {
        if (results.is_liked === "yes") {
          icon.src = "https://img.icons8.com/plasticine/100/000000/like.png";
          element.setAttribute("data-is_liked", "yes");
        } else {
          icon.src =
            "https://img.icons8.com/carbon-copy/100/000000/like--v2.png";
          element.setAttribute("data-is_liked", "no");
        }
        count.textContent = results.like_count;
      }
    })
    .catch(function (results) {
      alert("Network Error. Please Check your connection.");
    });
  });
}
