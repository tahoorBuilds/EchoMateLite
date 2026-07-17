document.addEventListener("DOMContentLoaded", () => {

    // LIKE / UNLIKE
    document.querySelectorAll(".like-btn").forEach(btn => {

        btn.addEventListener("click", async function(e){

            e.preventDefault();

            const res = await fetch(this.href);
            const data = await res.json();

            if(!data.success) return;

            const postId = this.href.split("/").pop();

            const heart = document.getElementById("heart-" + postId);
            const likes = document.getElementById("likes-" + postId);

            if(data.liked){

                heart.classList.remove("bi-heart");
                heart.classList.add("bi-heart-fill");
                heart.classList.add("text-danger");

                this.href = "/unlike/" + postId;

            }else{

                heart.classList.remove("bi-heart-fill");
                heart.classList.remove("text-danger");
                heart.classList.add("bi-heart");

                this.href = "/like/" + postId;

            }

            likes.innerHTML =
                data.likes + (data.likes == 1 ? " like" : " likes");

        });

    });


    // COMMENT
    document.querySelectorAll(".comment-form").forEach(form => {

        form.addEventListener("submit", async function(e){

            e.preventDefault();

            const formData = new FormData(this);

            const res = await fetch(this.action,{
                method:"POST",
                body:formData
            });

            const data = await res.json();

            if(!data.success) return;

            const commentsTitle = this.parentElement.nextElementSibling;
            const commentsContainer = commentsTitle.nextElementSibling;

            const div = document.createElement("div");

            div.className = "border rounded p-2 mb-2 bg-light";
            div.id = "comment-" + data.comment_id;

            div.innerHTML = `
                <strong>${data.username}</strong><br>
                ${data.comment}

                <div class="mt-2">
                    <a href="/deletecomment/${data.comment_id}/${this.dataset.post}"
                       class="delete-comment text-danger text-decoration-none">
                        <i class="bi bi-trash3 fs-5"></i>
                    </a>
                </div>
            `;

            commentsContainer.prepend(div);

            this.reset();

        });

    });


    // DELETE COMMENT (works for old + new comments)
   document.addEventListener("click", async function(e){

    const btn = e.target.closest(".delete-comment");

    if(!btn) return;

    e.preventDefault();

    const res = await fetch(btn.href);
    const data = await res.json();

    if(!data.success) return;

    btn.closest("[id^='comment-']").remove();

});


    // COMMENT BUTTON
document.querySelectorAll(".comment-btn").forEach(btn => {

    btn.addEventListener("click", function(e){

        e.preventDefault();

        const postId = this.dataset.post;

        const input = document.querySelector(
            `#comment${postId} input[name="comment"]`
        );

        if(input){
            input.focus();
        }

    });

});

});