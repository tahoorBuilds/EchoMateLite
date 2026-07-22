document.addEventListener("DOMContentLoaded", () => {

// LIKE / UNLIKE DYNAMIC AJAX SYSTEM
document.querySelectorAll(".like-btn").forEach(btn => {
    btn.addEventListener("click", async function(e){
        e.preventDefault();

        // Safe URL allocation
        const currentHref = this.getAttribute("href");
        const res = await fetch(currentHref);
        const data = await res.json();

        if(!data.success) return;

        // Extracting numbers safely using regex matching digits
        const postId = currentHref.match(/\d+/)[0]; 
        
        const heart = document.getElementById("heart-" + postId);
        const likes = document.getElementById("likes-" + postId);

        // Core dynamic behavior toggling based on backend response
        if(data.liked){
            heart.classList.remove("bi-heart");
            heart.classList.add("bi-heart-fill");
            this.setAttribute("href", "/unlike/" + postId);
        } else {
            heart.classList.remove("bi-heart-fill");
            heart.classList.add("bi-heart");
            this.setAttribute("href", "/like/" + postId);
        }

        // Updating frontend counters instantly
        if(likes) {
            likes.innerHTML = data.likes + (data.likes == 1 ? " like" : " likes");
        }
    });
});


// ==========================================
// COMMENT SYSTEM (UPDATED FOR LOOP UI)
// ==========================================
document.querySelectorAll(".comment-form").forEach(form => {
    form.addEventListener("submit", async function(e){
        e.preventDefault();

        const formData = new FormData(this);
        const submitBtn = this.querySelector('button[type="submit"]');
        
        // Button loading effect
        submitBtn.disabled = true;
        submitBtn.innerText = '...';

        try {
            const res = await fetch(this.action, {
                method: "POST",
                body: formData
            });

            const data = await res.json();

            if(!data.success) return;

            // Naye HTML structure ke hisaab se comments list dhoondhna
            const commentsContainer = this.previousElementSibling; 

            const div = document.createElement("div");
            div.className = "d-flex justify-content-between align-items-start mb-2";
            div.id = "comment-" + data.comment_id;

            // Naya Premium Aesthetic Comment Design
            div.innerHTML = `
                <div>
                    <strong style="font-size: 13px;">${data.username}</strong>
                    <span class="ms-1" style="font-size: 13px; color: #475569;">${data.comment}</span>
                </div>
                <a href="/deletecomment/${data.comment_id}/${this.dataset.post}" class="delete-comment text-danger opacity-75 text-decoration-none ms-2">
                    <i class="bi bi-trash3" style="font-size: 12px;"></i>
                </a>
            `;

            // Comment ko list me sabse neeche add karo
            commentsContainer.appendChild(div);
            
            // Scroll to bottom taaki naya comment dikhe
            commentsContainer.scrollTop = commentsContainer.scrollHeight;

            this.reset();
        } catch(error) {
            console.error("Comment Error:", error);
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerText = 'Post';
        }
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

// ==========================================
// IN-APP DM SHARE SYSTEM (INSTAGRAM STYLE)
// ==========================================

let currentSharePostId = null;

// 1. Share Button Dabane Par Modal Kholo
document.querySelectorAll(".share-btn").forEach(btn => {
    btn.addEventListener("click", function(e){
        e.preventDefault();
        currentSharePostId = this.getAttribute("data-post-id");
        document.getElementById("shareModal").style.display = "flex";
        loadShareUsers();
    });
});

// 2. Modal Band Karne Ka Function
function closeShareModal() {
    document.getElementById("shareModal").style.display = "none";
}

// 3. Database Se Users Load Karo
async function loadShareUsers() {
    const listDiv = document.getElementById("shareUsersList");
    listDiv.innerHTML = "<div class='text-center text-muted py-3'>Loading friends...</div>";
    
    const res = await fetch("/get_users_to_share");
    const data = await res.json();
    
    if (data.success) {
        listDiv.innerHTML = "";
        
        if (data.users.length === 0) {
            listDiv.innerHTML = "<div class='text-center text-muted py-3'>Follow some people to share posts!</div>";
            return;
        }
        
        // Har user ke aage "Send" button lagao
        data.users.forEach(user => {
            listDiv.innerHTML += `
                <div class="share-user-item">
                    <div class="fw-bold text-dark">@${user.username}</div>
                    <button class="btn-send-dm" onclick="sendPostInDM(${user.id}, this)">Send</button>
                </div>
            `;
        });
    }
}

// 4. API Hit Karke Post DM Me Bhejo
async function sendPostInDM(receiverId, btnElement) {
    btnElement.disabled = true;
    btnElement.innerText = "Sending...";
    
    const res = await fetch("/share_post_to_user", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            receiver_id: receiverId,
            post_id: currentSharePostId
        })
    });
    
    const data = await res.json();
    if (data.success) {
        btnElement.innerText = "Sent";
        btnElement.classList.add("sent");
    } else {
        btnElement.innerText = "Send";
        btnElement.disabled = false;
        alert("Failed to send post.");
    }
}
document.addEventListener("DOMContentLoaded", function() {
    const storyInput = document.getElementById('storyInput');
    if (storyInput) {
        storyInput.addEventListener('change', function() {
            console.log("File detected, submitting form...");
            document.getElementById('storyForm').submit();
        });
    }
});
