from flask import Flask, render_template, request, redirect, session, jsonify
import mysql.connector
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from s3_helper import upload_file_to_s3

@app.route('/test-upload', methods=['GET', 'POST'])
def test_upload():
    if request.method == 'POST':
        # Form se aayi hui file ko pakadna
        if 'file' not in request.files:
            return "Koi file nahi mili!"
            
        file = request.files['file']
        
        if file.filename != '':
            # Apne s3_helper wale function ko call karna
            file_url = upload_file_to_s3(file, file.filename)
            
            if file_url:
                return f"<h3>Success! 🚀</h3> File cloud par live hai: <a href='{file_url}' target='_blank'>{file_url}</a>"
            else:
                return "Upload fail ho gaya, terminal logs check karo."
            
    # GET request par ek simple sa HTML form dikhana
    return '''
    <h2>AWS S3 Upload Test</h2>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="file">
      <br><br>
      <input type="submit" value="Upload to AWS S3">
    </form>
    '''

# Define allowed format groups
ALLOWED_IMAGES = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
ALLOWED_VIDEOS = {'.mp4', '.mov', '.avi', '.mkv', '.webm'}

app = Flask(__name__)
app.secret_key = "echomatelite_secret_key"

UPLOAD_FOLDER = os.path.join(
    app.root_path,
    "static",
    "profile_pics"
)

POST_FOLDER = os.path.join(app.root_path, "static", "post_images")
app.config["POST_FOLDER"] = POST_FOLDER
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ye line folders auto-create karegi agar wo nahi hain
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(POST_FOLDER, exist_ok=True)

try:
    db = mysql.connector.connect(
        host="db",           # <-- Docker service ka naam
        user="echo",         # <-- Compose file wala user
        password="echo123",  # <-- Compose file wala password
        database="echomatelite"
    )
    cursor = db.cursor(buffered=True)
    print("✅ Database Connected Successfully!")
except mysql.connector.Error as err:
    print(f"❌ Database Connection Error: {err}")
    db = None
    cursor = None

# Home Page
@app.route("/")
def home():
    # Agar user pehle se login hai, toh direct feed par bhejo
    if "user_id" in session:
        return redirect("/feed")
    
    # Agar login nahi hai, tabhi landing page dikhao
    return render_template("index.html")

# ==============================================================
# MERGED PROFILE ROUTE (Dashboard + Purana Profile Data)
# ==============================================================
@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect("/login")
    
    # Update Last Seen
    sql = "UPDATE users SET last_seen=NOW() WHERE id=%s"
    values = (session["user_id"],)
    cursor.execute(sql, values)
    db.commit()

    # User Info
    sql = "SELECT username, profile_pic, bio FROM users WHERE id=%s"
    cursor.execute(sql, values)
    user = cursor.fetchone()

    # Total Posts
    sql = "SELECT COUNT(*) FROM posts WHERE user_id=%s"
    cursor.execute(sql, values)
    total_posts = cursor.fetchone()[0]

    # My posts (User ke saare posts)
    sql = "SELECT id, content, image FROM posts WHERE user_id=%s ORDER BY id DESC"
    cursor.execute(sql, values)
    posts = cursor.fetchall()

    # Followers
    sql = "SELECT COUNT(*) FROM followers WHERE following_id=%s"
    cursor.execute(sql, values)
    followers_count = cursor.fetchone()[0]

    # Following
    sql = "SELECT COUNT(*) FROM followers WHERE follower_id=%s"
    cursor.execute(sql, values)
    following_count = cursor.fetchone()[0]

    # Notifications Count
    sql = "SELECT COUNT(*) FROM notifications WHERE user_id=%s"
    cursor.execute(sql, values)
    notifications_count = cursor.fetchone()[0]  

    return render_template(
        "profile.html",  
        user=user,
        posts=posts,
        total_posts=total_posts,
        followers_count=followers_count,
        following_count=following_count,
        notifications_count=notifications_count
    )

@app.route("/editbio", methods=["GET", "POST"])
def editbio():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        bio = request.form["bio"]
        sql = "UPDATE users SET bio=%s WHERE id=%s"
        values = (bio, session["user_id"])
        cursor.execute(sql, values)
        db.commit()
        return redirect("/profile")

    return render_template("editbio.html")

# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        values = (username, email, hashed_password)
        cursor.execute(sql, values)
        db.commit()

        return "Registration Successful!"

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        print("EMAIL =", email)
        print("PASSWORD =", password)

        try:
            db.ping(reconnect=True, attempts=3, delay=2)
            sql = "SELECT * FROM users WHERE email=%s"
            values = (email,)
            cursor.execute(sql, values)
            user = cursor.fetchone()

            print("USER =", user)

            if user:
                print("DATABASE PASSWORD =", user[3])
                
                # SMART PASSWORD CHECKER: Supports both Hashed and Plain Text passwords
                password_valid = False
                db_password = str(user[3])
                
                if db_password.startswith("pbkdf2:") or db_password.startswith("scrypt$"):
                    if check_password_hash(db_password, password):
                        password_valid = True
                else:
                    # Fallback for plain text passwords in database
                    if db_password == password:
                        password_valid = True
                
                if password_valid:
                    session["user_id"] = user[0]
                    session["username"] = user[1]
                    session["profile_pic"] = user[5]
                    print(user)
                    print(session["profile_pic"])
                    
                    # Login ke baad seedha feed par bhejega
                    return redirect("/feed")
                else:
                    return "Wrong Password!"
            else:
                return "Email Not Found!"

        except Exception as e:
            return f"Login Error: {str(e)}"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/uploadprofilepic", methods=["POST"])
def uploadprofilepic():
    if "user_id" not in session:
        return redirect("/login")

    file = request.files["profile_pic"]

    if file.filename == "":
        return redirect("/profile")

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    sql = "UPDATE users SET profile_pic=%s WHERE id=%s"
    values = (filename, session["user_id"])
    cursor.execute(sql, values)
    db.commit()

    return redirect("/profile")   

# Story Upload Route
@app.route("/upload_story", methods=["POST"])
def upload_story():
    if "user_id" not in session:
        return "Please login", 401
    
    if 'story_media' not in request.files:
        print("ERROR: 'story_media' field nahi mila form se!")
        return "No file part", 400
        
    file = request.files['story_media']
    
    if file.filename == '':
        print("ERROR: File ka naam khali hai!")
        return "No selected file", 400
        
    if file:
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config["POST_FOLDER"], filename)
        file.save(save_path)
        
        sql = "INSERT INTO stories (user_id, media_url) VALUES (%s, %s)"
        cursor.execute(sql, (session["user_id"], filename))
        db.commit()
        
        print(f"SUCCESS: Story saved at {save_path}")
        return redirect("/feed")

@app.route("/view_story/<int:user_id>")
def view_story(user_id):
    if "user_id" not in session:
        return redirect("/login")
    
    # Ab hum 'id' bhi select kar rahe hain delete karne ke liye
    sql = """
    SELECT id, media_url, created_at 
    FROM stories 
    WHERE user_id = %s AND created_at >= NOW() - INTERVAL 24 HOUR
    ORDER BY created_at ASC
    """
    cursor.execute(sql, (user_id,))
    user_stories = cursor.fetchall()
    
    # User ki details mein id bhi le rahe hain
    cursor.execute("SELECT id, username, profile_pic FROM users WHERE id = %s", (user_id,))
    story_user = cursor.fetchone()
    
    return render_template("view_story.html", stories=user_stories, story_user=story_user, current_user_id=session["user_id"])

# --- NAYA DELETE ROUTE YAHAN ADD KAREIN ---

@app.route("/delete_story/<int:story_id>")
def delete_story(story_id):
    if "user_id" not in session:
        return redirect("/login")
        
    # MASTER DELETE: Teri saari pichli upload ki hui stories ek baar mein saaf
    sql = "DELETE FROM stories WHERE user_id=%s"
    cursor.execute(sql, (session["user_id"],))
    db.commit()
    
    return redirect("/feed")

@app.route("/createpost", methods=["GET", "POST"])
def createpost():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        print("POST RECEIVED")
        content = request.form.get("content", "")
        
        file = request.files.get("image")
        file_name = None

        if file and file.filename:
            _, ext = os.path.splitext(file.filename.lower())
            
            file.seek(0, os.SEEK_END)
            file_length = file.tell()
            file.seek(0) 

            if ext in ALLOWED_IMAGES:
                if file_length > 5 * 1024 * 1024:
                    return "Error: Image file size exceeds maximum limit of 5MB", 400
                file_name = secure_filename(file.filename)
                
            elif ext in ALLOWED_VIDEOS:
                if file_length > 50 * 1024 * 1024:
                    return "Error: Video file size exceeds maximum limit of 50MB", 400
                file_name = secure_filename(file.filename)
            else:
                return "Error: Unsupported file format.", 400

            print(f"Uploading media: {file_name} (Size: {file_length} bytes)")
            # FIXED: Saved to absolute dynamic path
            file.save(os.path.join(app.config["POST_FOLDER"], file_name))

        user_id = session["user_id"]

        try:
            sql = """
            INSERT INTO posts (content, user_id, image)
            VALUES (%s, %s, %s)
            """
            values = (content, user_id, file_name)
            cursor.execute(sql, values)
            db.commit()
            
            print("POST SAVED SUCCESSFULLY")
            return redirect("/feed")

        except Exception as e:
            print("DATABASE ERROR:", e)
            return f"Error Creating Post: {e}", 500

    return render_template("createpost.html")

@app.route("/savepost/<int:post_id>")
def savepost(post_id):

    if "user_id" not in session:
        return redirect("/login")

    sql = """
    INSERT INTO saved_posts (user_id, post_id)
    VALUES (%s, %s)
    """

    values = (
        session["user_id"],
        post_id
    )

    cursor.execute(sql, values)
    db.commit()

    return redirect("/feed")

@app.route("/myposts")
def myposts():

    if "user_id" not in session:
        return redirect("/login")

    sql = """
    SELECT id, content, image
    FROM posts
    WHERE user_id=%s
    ORDER BY id DESC
    """

    cursor.execute(sql, (session["user_id"],))

    posts = cursor.fetchall()

    return render_template(
        "myposts.html",
        posts=posts
    )

@app.route("/feed")
def feed():

    if "user_id" not in session:
        return redirect("/login")

    # Feed Posts
    sql = """
    SELECT
        posts.id,
        posts.content,
        users.username,
        users.profile_pic,
        posts.created_at,
        COUNT(DISTINCT likes.id) AS total_likes,
        posts.image,
        users.id
    FROM posts

    JOIN users
    ON posts.user_id = users.id

    LEFT JOIN likes
    ON posts.id = likes.post_id

    WHERE
        posts.user_id = %s
        OR posts.user_id IN (
            SELECT following_id
            FROM followers
            WHERE follower_id = %s
        )

    GROUP BY posts.id

    ORDER BY posts.id DESC
    """

    values = (
        session["user_id"],
        session["user_id"]
    )

    cursor.execute(sql, values)

    posts = cursor.fetchall()

    # Like Status
    posts_with_like_status = []

    for post in posts:

        liked = False

        sql = """
        SELECT id
        FROM likes
        WHERE user_id=%s AND post_id=%s
        """

        values = (
            session["user_id"],
            post[0]
        )

        cursor.execute(sql, values)

        if cursor.fetchone():
            liked = True

        posts_with_like_status.append(post + (liked,))

    # Comments
    all_comments = {}

    for post in posts:

        sql = """
        SELECT
            comments.comment,
            users.username,
            comments.id,
            comments.user_id
        FROM comments

        JOIN users
        ON comments.user_id = users.id

        WHERE comments.post_id=%s

        ORDER BY comments.id DESC
        """

        values = (post[0],)

        cursor.execute(sql, values)

        all_comments[post[0]] = cursor.fetchall()

    # Comment Count
    comment_counts = {}

    for post in posts:

        sql = """
        SELECT COUNT(*)
        FROM comments
        WHERE post_id=%s
        """

        values = (post[0],)

        cursor.execute(sql, values)

        comment_counts[post[0]] = cursor.fetchone()[0]

    # Trending Posts
    sql = """
    SELECT
        posts.id,
        posts.content,
        users.username,
        COUNT(likes.id) AS total_likes
    FROM posts

    JOIN users
    ON posts.user_id = users.id

    LEFT JOIN likes
    ON posts.id = likes.post_id

    GROUP BY posts.id

    ORDER BY total_likes DESC

    LIMIT 5
    """

    cursor.execute(sql)

    trending_posts = cursor.fetchall()

    # Fetch REAL users the current user is following for the "Stories/Loops" section
    sql_stories = """
    SELECT users.id, users.username, users.profile_pic 
    FROM followers 
    JOIN users ON followers.following_id = users.id 
    WHERE followers.follower_id = %s
    """
    cursor.execute(sql_stories, (session["user_id"],))
    following_users = cursor.fetchall()

    # Fetch stories (last 24 hours), Grouped by User
    sql_stories = """
    SELECT stories.user_id, MAX(stories.media_url), users.username, users.profile_pic
    FROM stories
    JOIN users ON stories.user_id = users.id
    WHERE (stories.user_id = %s OR stories.user_id IN (
        SELECT following_id FROM followers WHERE follower_id = %s
    ))
    AND stories.created_at >= NOW() - INTERVAL 24 HOUR
    GROUP BY stories.user_id, users.username, users.profile_pic
    """
    
    cursor.execute(sql_stories, (session["user_id"], session["user_id"]))
    stories = cursor.fetchall()

    return render_template(
        "feed.html",
        posts=posts_with_like_status,
        all_comments=all_comments,
        comment_counts=comment_counts,
        trending_posts=trending_posts,
        following_users=following_users,
        stories=stories 
    )

@app.route("/deletepost/<int:post_id>")
def deletepost(post_id):

    if "user_id" not in session:
        return jsonify({"success": False}), 401

    sql = "DELETE FROM posts WHERE id=%s AND user_id=%s"
    values = (post_id, session["user_id"])

    cursor.execute(sql, values)
    db.commit()

    return jsonify({
        "success": True,
        "post_id": post_id
    })

@app.route("/like/<int:post_id>")
def like(post_id):
    if "user_id" not in session:
        return jsonify({"success": False}), 401

    try:
        # Connection check taaki server drop hone par error na aaye
        db.ping(reconnect=True, attempts=3, delay=2)

        # Check karein ki user ne pehle se like kiya hai ya nahi
        sql = "SELECT id FROM likes WHERE user_id=%s AND post_id=%s"
        cursor.execute(sql, (session["user_id"], post_id))
        already_liked = cursor.fetchone()

        if already_liked:
            # UNLIKE: Agar liked hai toh delete kar do
            sql_del = "DELETE FROM likes WHERE user_id=%s AND post_id=%s"
            cursor.execute(sql_del, (session["user_id"], post_id))
            db.commit()
            is_liked = False
        else:
            # LIKE: Agar liked nahi hai toh insert kar do
            sql_ins = "INSERT INTO likes (user_id, post_id) VALUES (%s, %s)"
            cursor.execute(sql_ins, (session["user_id"], post_id))
            db.commit()

            # Post owner ko notification bhejo
            cursor.execute("SELECT user_id FROM posts WHERE id=%s", (post_id,))
            post_owner = cursor.fetchone()

            if post_owner and post_owner[0] != session["user_id"]:
                notification = f"{session['username']} liked your post"
                target_url = f"/feed#post{post_id}"
                sql_notif = "INSERT INTO notifications (user_id, message, target_url) VALUES (%s, %s, %s)"
                cursor.execute(sql_notif, (post_owner[0], notification, target_url))
                db.commit()
            
            is_liked = True

        # Delete ya Insert ke baad naya total count nikal lo
        cursor.execute("SELECT COUNT(*) FROM likes WHERE post_id=%s", (post_id,))
        total_likes_result = cursor.fetchone()
        total_likes = total_likes_result[0] if total_likes_result else 0

        return jsonify({
            "success": True,
            "liked": is_liked,
            "likes": total_likes
        })

    except Exception as e:
        print(f"LIKE ERROR: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/postlikes/<int:post_id>")
def postlikes(post_id):

    if "user_id" not in session:
        return redirect("/login")

    sql = """
    SELECT users.username
    FROM likes
    JOIN users
    ON likes.user_id = users.id
    WHERE likes.post_id=%s
    """

    values = (post_id,)

    cursor.execute(sql, values)

    users = cursor.fetchall()

    return render_template(
        "postlikes.html",
        users=users
    )

@app.route("/unlike/<int:post_id>")
def unlike(post_id):

    if "user_id" not in session:
        return jsonify({"success": False}), 401

    sql = """
    DELETE FROM likes
    WHERE user_id=%s AND post_id=%s
    """

    values = (
        session["user_id"],
        post_id
    )

    cursor.execute(sql, values)
    db.commit()

    # Total likes after unlike
    sql = """
    SELECT COUNT(*)
    FROM likes
    WHERE post_id=%s
    """

    cursor.execute(sql, (post_id,))
    total_likes = cursor.fetchone()[0]

    return jsonify({
    "success": True,
    "liked": False,
    "likes": total_likes
})

@app.route("/comment/<int:post_id>", methods=["POST"])
def comment(post_id):

    if "user_id" not in session:
        return jsonify({"success": False}), 401

    comment_text = request.form["comment"]

    sql = """
    INSERT INTO comments (comment, user_id, post_id)
    VALUES (%s, %s, %s)
    """

    values = (
        comment_text,
        session["user_id"],
        post_id
    )

    cursor.execute(sql, values)
    db.commit()

    comment_id = cursor.lastrowid

    # Get post owner
    sql = """
    SELECT user_id
    FROM posts
    WHERE id=%s
    """

    cursor.execute(sql, (post_id,))
    post_owner = cursor.fetchone()[0]

    if post_owner != session["user_id"]:

        notification = f"{session['username']} commented on your post"
        target_url = f"/feed#post{post_id}"

        sql = """
        INSERT INTO notifications (user_id, message, target_url)
        VALUES (%s, %s, %s)
        """

        cursor.execute(sql, (post_owner, notification, target_url))
        db.commit()

    return jsonify({
    "success": True,
    "comment": comment_text,
    "username": session["username"],
    "user_id": session["user_id"],
    "comment_id": comment_id
})

@app.route("/deletecomment/<int:comment_id>/<int:post_id>")
def deletecomment(comment_id, post_id):

    if "user_id" not in session:
        return redirect("/login")

    sql = """
    DELETE FROM comments
    WHERE id=%s AND user_id=%s
    """

    values = (
        comment_id,
        session["user_id"]
    )

    cursor.execute(sql, values)
    db.commit()

    return jsonify({
    "success": True,
    "comment_id": comment_id
})

@app.route("/editcomment/<int:comment_id>", methods=["GET", "POST"])
def editcomment(comment_id):

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        new_comment = request.form["comment"]

        sql = """
        UPDATE comments
        SET comment=%s
        WHERE id=%s AND user_id=%s
        """

        values = (
            new_comment,
            comment_id,
            session["user_id"]
        )

        cursor.execute(sql, values)
        db.commit()

        return redirect("/feed")

    sql = """
    SELECT comment
    FROM comments
    WHERE id=%s AND user_id=%s
    """

    values = (
        comment_id,
        session["user_id"]
    )

    cursor.execute(sql, values)

    comment = cursor.fetchone()

    return render_template(
        "editcomment.html",
        comment=comment,
        comment_id=comment_id
    )

@app.route("/editpost/<int:post_id>", methods=["GET", "POST"])
def editpost(post_id):

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        content = request.form["content"]

        sql = """
        UPDATE posts
        SET content=%s
        WHERE id=%s AND user_id=%s
        """

        values = (content, post_id, session["user_id"])

        cursor.execute(sql, values)
        db.commit()

        return redirect("/profile")

    sql = """
    SELECT content
    FROM posts
    WHERE id=%s AND user_id=%s
    """

    values = (post_id, session["user_id"])

    cursor.execute(sql, values)

    post = cursor.fetchone()

    return render_template("editpost.html", post=post)

@app.route("/searchuser", methods=["GET", "POST"])
def searchuser():
    users = []
    if request.method == "POST":
        # .strip() se extra spaces hat jate hain
        username = request.form.get("username", "").strip()
        
        # LIKE '%...%' use karne se partial match ho jata hai
        sql = "SELECT id, username, profile_pic FROM users WHERE username LIKE %s"
        values = (f"%{username}%",)
        cursor.execute(sql, values)
        users = cursor.fetchall()

    return render_template("searchuser.html", users=users)

@app.route("/user/<int:user_id>")
def userprofile(user_id):
    if "user_id" not in session:
        return redirect("/login")

    # User Info
    sql = "SELECT id, username, last_seen, profile_pic FROM users WHERE id=%s"
    cursor.execute(sql, (user_id,))
    user = cursor.fetchone()

    if not user:
        return "User Not Found"

    # 1. User Posts ke sath Total Likes bhi fetch karo
    sql = """
    SELECT 
        posts.id, 
        posts.content, 
        posts.image,
        COUNT(likes.id) AS total_likes
    FROM posts
    LEFT JOIN likes ON posts.id = likes.post_id
    WHERE posts.user_id = %s
    GROUP BY posts.id
    ORDER BY posts.id DESC
    """
    cursor.execute(sql, (user_id,))
    raw_posts = cursor.fetchall()

    # 2. Har post ke liye check karo ki logged-in user ne like kiya hai ya nahi
    posts = []
    for p in raw_posts:
        post_id = p[0]
        liked = False
        cursor.execute("SELECT id FROM likes WHERE user_id=%s AND post_id=%s", (session["user_id"], post_id))
        if cursor.fetchone():
            liked = True
        
        # Tuple mein 'liked' status (True/False) jod do
        posts.append(p + (liked,))

    # Followers Count
    cursor.execute("SELECT COUNT(*) FROM followers WHERE following_id=%s", (user_id,))
    followers_count = cursor.fetchone()[0]

    # Following Count
    cursor.execute("SELECT COUNT(*) FROM followers WHERE follower_id=%s", (user_id,))
    following_count = cursor.fetchone()[0]

    # Follow Status
    is_following = False
    cursor.execute("SELECT * FROM followers WHERE follower_id=%s AND following_id=%s", (session["user_id"], user_id))
    if cursor.fetchone():
        is_following = True

    # Share Modal users list
    cursor.execute("SELECT id, username FROM users WHERE id != %s", (session["user_id"],))
    all_users = cursor.fetchall()

    return render_template(
        "userprofile.html",
        user=user,
        posts=posts,
        followers_count=followers_count,
        following_count=following_count,
        is_following=is_following,
        all_users=all_users,
        now=datetime.now()
    )

@app.route("/follow/<int:user_id>")
def follow(user_id):

    if "user_id" not in session:
        return redirect("/login")

    if session["user_id"] == user_id:
        return redirect(f"/user/{user_id}")

    sql = """
    SELECT *
    FROM followers
    WHERE follower_id=%s AND following_id=%s
    """

    values = (session["user_id"], user_id)

    cursor.execute(sql, values)

    already_following = cursor.fetchone()

    if already_following:
        return redirect(f"/user/{user_id}")

    sql = """
    INSERT INTO followers (follower_id, following_id)
    VALUES (%s, %s)
    """

    values = (session["user_id"], user_id)

    cursor.execute(sql, values)
    db.commit()

   # Notification
    notification = f"{session['username']} followed you"
    
    # FIXED: /userprofile ki jagah /user aayega
    target_url = f"/user/{session['user_id']}"

    sql = """
    INSERT INTO notifications (user_id, message, target_url)
    VALUES (%s, %s, %s)
    """

    values = (user_id, notification, target_url)

    cursor.execute(sql, values)
    db.commit()

    return redirect(f"/user/{user_id}")

@app.route("/admin")
def admin():

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM posts")
    total_posts = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM likes")
    total_likes = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM comments")
    total_comments = cursor.fetchone()[0]

    return render_template(
        "admin.html",
        total_users=total_users,
        total_posts=total_posts,
        total_likes=total_likes,
        total_comments=total_comments
    )

@app.route("/unfollow/<int:user_id>")
def unfollow(user_id):

    if "user_id" not in session:
        return redirect("/login")

    sql = """
    DELETE FROM followers
    WHERE follower_id=%s AND following_id=%s
    """

    values = (session["user_id"], user_id)

    cursor.execute(sql, values)
    db.commit()

    return redirect(f"/user/{user_id}")

# FOLLOWERS ROUTE (UPDATED)
@app.route("/followers/<int:profile_id>")
def followers(profile_id):
    if "user_id" not in session:
        return redirect("/login")

    sql = """
    SELECT users.id, users.username, users.profile_pic
    FROM followers
    JOIN users ON followers.follower_id = users.id
    WHERE followers.following_id=%s
    """
    cursor.execute(sql, (profile_id,))
    followers = cursor.fetchall()
    
    return render_template("followers.html", followers=followers)

# FOLLOWING ROUTE (UPDATED)
@app.route("/following/<int:profile_id>")
def following(profile_id):
    if "user_id" not in session:
        return redirect("/login")

    sql = """
    SELECT users.id, users.username, users.profile_pic
    FROM followers
    JOIN users ON followers.following_id = users.id
    WHERE followers.follower_id=%s
    """
    cursor.execute(sql, (profile_id,))
    following = cursor.fetchall()
    
    return render_template("following.html", following=following)

@app.route("/notifications")
def notifications():

    if "user_id" not in session:
        return redirect("/login")

    sql = """
    SELECT message, target_url, created_at
    FROM notifications
    WHERE user_id=%s
    ORDER BY id DESC
    """

    values = (session["user_id"],)

    cursor.execute(sql, values)

    notifications = cursor.fetchall()

    return render_template(
        "notifications.html",
        notifications=notifications
    )

@app.route("/sendmessage/<int:user_id>", methods=["GET", "POST"])
def sendmessage(user_id):

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        message = request.form["message"]

        sql = """
        INSERT INTO messages
        (sender_id, receiver_id, message)
        VALUES (%s, %s, %s)
        """

        values = (
            session["user_id"],
            user_id,
            message
        )

        cursor.execute(sql, values)
        db.commit()

        sql = """
        INSERT INTO notifications
        (user_id, message, target_url)
        VALUES (%s, %s, %s)
        """

        values = (
        user_id,
        "You received a new message",
        f"/chat/{session['user_id']}"
    )

        cursor.execute(sql, values)
        db.commit()

        return redirect(f"/chat/{user_id}")

    return render_template(
        "sendmessage.html",
        user_id=user_id
    )

@app.route("/inbox")
def inbox():
    if "user_id" not in session:
        return redirect("/login")

    # FIXED: Ab ye query dono layegi - jinko tumne bheja hai aur jinhone tumhe bheja hai
    sql = """
    SELECT DISTINCT users.id, users.username 
    FROM messages 
    JOIN users ON (users.id = messages.sender_id OR users.id = messages.receiver_id)
    WHERE (messages.sender_id = %s OR messages.receiver_id = %s)
    AND users.id != %s
    ORDER BY users.username
    """

    # Values 3 baar pass karni hongi kyunki %s teen baar use hua hai
    values = (session["user_id"], session["user_id"], session["user_id"])

    cursor.execute(sql, values)
    chats = cursor.fetchall()

    return render_template("inbox.html", chats=chats)

@app.route("/chat/<int:user_id>")
def chat(user_id):
    if "user_id" not in session:
        return redirect("/login")

    # Pehle saare messages nikalo
    sql = """
    SELECT messages.id, messages.message, users.username, messages.sender_id, messages.created_at
    FROM messages
    JOIN users ON messages.sender_id = users.id
    WHERE (messages.sender_id=%s AND messages.receiver_id=%s)
       OR (messages.sender_id=%s AND messages.receiver_id=%s)
    ORDER BY messages.id
    """
    values = (session["user_id"], user_id, user_id, session["user_id"])
    cursor.execute(sql, values)
    raw_messages = cursor.fetchall()

    # Smart Message Parser
    messages = []
    for msg in raw_messages:
        msg_id, text, username, sender_id, created_at = msg
        post_data = None
        
        # Agar message me POST_SHARE ka tag hai, toh post dhoondho
        if text.startswith("POST_SHARE:"):
            post_id = text.split(":")[1]
            sql_post = "SELECT id, image, content, user_id FROM posts WHERE id=%s"
            cursor.execute(sql_post, (post_id,))
            post_data = cursor.fetchone()
        
        # Dictionary bana kar frontend ko bhejo
        messages.append({
            "id": msg_id,
            "text": text,
            "username": username,
            "sender_id": sender_id,
            "created_at": created_at,
            "post": post_data
        })

    return render_template("chat.html", messages=messages, user_id=user_id)

@app.route("/deletemessage/<int:message_id>/<int:user_id>")
def deletemessage(message_id, user_id):

    if "user_id" not in session:
        return redirect("/login")

    sql = """
    DELETE FROM messages
    WHERE id=%s AND sender_id=%s
    """

    values = (
        message_id,
        session["user_id"]
    )

    cursor.execute(sql, values)
    db.commit()

    return redirect(f"/chat/{user_id}")

# ==========================================
# INSTAGRAM STYLE IN-APP SHARE FEATURE
# ==========================================

@app.route("/get_users_to_share")
def get_users_to_share():
    if "user_id" not in session:
        return jsonify({"success": False}), 401
    
    # Un users ko laao jinhe current user follow karta hai
    sql = """
    SELECT users.id, users.username 
    FROM followers 
    JOIN users ON followers.following_id = users.id 
    WHERE followers.follower_id=%s
    """
    cursor.execute(sql, (session["user_id"],))
    users = cursor.fetchall()
    
    user_list = [{"id": u[0], "username": u[1]} for u in users]
    return jsonify({"success": True, "users": user_list})

@app.route("/share_post_to_user", methods=["POST"])
def share_post_to_user():
    if "user_id" not in session:
        return jsonify({"success": False}), 401
    
    data = request.get_json()
    receiver_id = data.get("receiver_id")
    post_id = data.get("post_id")
    
    # FIXED: Ab hum link nahi, ek hidden format tag bhejenge
    message = f"POST_SHARE:{post_id}"
    
    sql = "INSERT INTO messages (sender_id, receiver_id, message) VALUES (%s, %s, %s)"
    cursor.execute(sql, (session["user_id"], receiver_id, message))
    db.commit()
    
    notif_msg = f"{session['username']} shared a post with you"
    target_url = f"/chat/{session['user_id']}"
    sql = "INSERT INTO notifications (user_id, message, target_url) VALUES (%s, %s, %s)"
    cursor.execute(sql, (receiver_id, notif_msg, target_url))
    db.commit()
    
    return jsonify({"success": True})

@app.route('/watch_live/<room_id>')
def watch_live(room_id):
    # User ID aur Username session se le rahe hain
    user_id = session.get('user_id', 'Guest123')
    username = session.get('username', 'Guest User')
    return render_template('live.html', room_id=room_id, user_id=user_id, username=username)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)