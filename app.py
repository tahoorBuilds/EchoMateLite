from flask import Flask, render_template, request, redirect, session
import mysql.connector
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "echomatelite_secret_key"

import os

UPLOAD_FOLDER = os.path.join(
    app.root_path,
    "static",
    "profile_pics"
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
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
    return render_template("index.html")


# Database Test
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")
    
    sql = """
    UPDATE users
    SET last_seen=NOW()
    WHERE id=%s
    """

    values = (session["user_id"],)

    cursor.execute(sql, values)
    db.commit()

    # User Info
    sql = """
    SELECT username, profile_pic, bio
    FROM users
    WHERE id=%s
    """

    values = (session["user_id"],)

    cursor.execute(sql, values)

    user = cursor.fetchone()

    # Total Posts
    sql = """
    SELECT COUNT(*)
    FROM posts
    WHERE user_id=%s
    """

    cursor.execute(sql, values)

    total_posts = cursor.fetchone()[0]

    # Followers
    sql = """
    SELECT COUNT(*)
    FROM followers
    WHERE following_id=%s
    """

    cursor.execute(sql, values)

    followers_count = cursor.fetchone()[0]

    # Following
    sql = """
    SELECT COUNT(*)
    FROM followers
    WHERE follower_id=%s
    """

    cursor.execute(sql, values)

    following_count = cursor.fetchone()[0]

    # Notifications Count
    sql = """
    SELECT COUNT(*)
    FROM notifications
    WHERE user_id=%s
    """ 

    cursor.execute(sql, values)

    notifications_count = cursor.fetchone()[0]  

    return render_template(
        "dashboard.html",
        user=user,
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

        sql = """
        UPDATE users
        SET bio=%s
        WHERE id=%s
        """

        values = (bio, session["user_id"])

        cursor.execute(sql, values)
        db.commit()

        return redirect("/profile")

    return render_template("editbio.html")

@app.route("/searchpost", methods=["GET", "POST"])
def searchpost():

    posts = []

    if request.method == "POST":

        keyword = request.form["keyword"]

        sql = """
        SELECT
            posts.id,
            posts.content,
            users.username,
            users.id,
            posts.image
          FROM posts

          JOIN users
          ON posts.user_id = users.id

          WHERE
          posts.content LIKE %s
          OR users.username LIKE %s

          ORDER BY posts.id DESC
          """

        values =(
                f"%{keyword}%",
                f"%{keyword}%"
            )

        cursor.execute(sql, values)

        posts = cursor.fetchall()
    
    return render_template(
        "searchpost.html",
        posts=posts
    )

# Register
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        values = (username, email, password)

        cursor.execute(sql, values)
        db.commit()

        return "Registration Successful!"

    return render_template("register.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        print("EMAIL =", email)
        print("PASSWORD =", password)

        try:

            sql = "SELECT * FROM users WHERE email=%s"
            values = (email,)

            cursor.execute(sql, values)

            user = cursor.fetchone()

            print("USER =", user)

            if user:

                print("DATABASE PASSWORD =", user[3])

                if password == user[3]:

                    session['user_id'] = user[0]
                    session['username'] = user[1]

                    return redirect("/dashboard")

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

    file.save(
        os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )
    )

    sql = """
    UPDATE users
    SET profile_pic=%s
    WHERE id=%s
    """

    values = (filename, session["user_id"])

    cursor.execute(sql, values)
    db.commit()

    return redirect("/profile")    


# Create Post
@app.route("/createpost", methods=["GET", "POST"])
def createpost():

    if request.method == "POST":

        if 'user_id' not in session:
            return redirect("/login")

        content = request.form["content"]

        image = request.files.get("image")
        image_name = None

        if image and image.filename:

            image_name = image.filename

            image.save(
                os.path.join(
                    "static/post_images",
                    image_name
                )
            )

        user_id = session.get('user_id')

        try:

            sql = """
            INSERT INTO posts (content, user_id, image)
            VALUES (%s, %s, %s)
            """

            values = (
                content,
                user_id,
                image_name
            )

            cursor.execute(sql, values)
            db.commit()

            return redirect("/feed")

        except Exception as e:
            return f"Error Creating Post: {str(e)}"

    return render_template("createpost.html")

@app.route("/feed")
def feed():
    if "user_id" not in session:
        return redirect("/login")

    sql = """
    SELECT
        posts.id,
        posts.content,
        users.username,
        posts.created_at,
        COUNT(DISTINCT likes.id) as total_likes,
        posts.image
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

    posts_with_like_status = []

    for post in posts:

        liked = False

        sql = """
        SELECT *
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

    all_comments = {}

    for post in posts:

        sql = """
        SELECT comments.comment, users.username
        FROM comments

        JOIN users
        ON comments.user_id = users.id

        WHERE comments.post_id=%s

        ORDER BY comments.id DESC
        """

        values = (post[0],)

        cursor.execute(sql, values)

        all_comments[post[0]] = cursor.fetchall()

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

    return render_template(
        "feed.html",
        posts=posts_with_like_status,
        all_comments=all_comments,
        comment_counts=comment_counts,
        trending_posts=trending_posts
    )

@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect("/login")

    sql = """
    UPDATE users
    SET last_seen=NOW()
    WHERE id=%s
    """

    values = (session["user_id"],)

    cursor.execute(sql, values)
    db.commit()

    sql = """
    SELECT username, profile_pic,bio
    FROM users
    WHERE id=%s
    """

    values = (session["user_id"],)

    cursor.execute(sql, values)

    user = cursor.fetchone()

    sql = """
    SELECT id, content
    FROM posts
    WHERE user_id=%s
    ORDER BY id DESC
    """

    values = (session["user_id"],)

    cursor.execute(sql, values)

    posts = cursor.fetchall()

    return render_template(
        "profile.html",
        posts=posts,
        user=user
    )

@app.route("/deletepost/<int:post_id>")
def deletepost(post_id):

    if "user_id" not in session:
        return redirect("/login")

    sql = "DELETE FROM posts WHERE id=%s AND user_id=%s"
    values = (post_id, session["user_id"])

    cursor.execute(sql, values)
    db.commit()

    return redirect("/feed")

@app.route("/like/<int:post_id>")
def like(post_id):

    if "user_id" not in session:
        return redirect("/login")

    sql = """
    SELECT *
    FROM likes
    WHERE user_id=%s AND post_id=%s

    """

    values = (session["user_id"], post_id)

    cursor.execute(sql, values)

    already_liked = cursor.fetchone()

    if not already_liked:

        sql = """
        INSERT INTO likes (user_id, post_id)
        VALUES (%s, %s)
        """

        cursor.execute(sql, values)
        db.commit()

        # Get post owner
        sql = """
        SELECT user_id
        FROM posts
        WHERE id=%s
        """

        values = (post_id,)

        cursor.execute(sql, values)

        post_owner = cursor.fetchone()[0]

        if post_owner != session["user_id"]:

            notification = f"{session['username']} liked your post"

            sql = """
            INSERT INTO notifications (user_id, message)
            VALUES (%s, %s)
            """

            values = (post_owner, notification)

            cursor.execute(sql, values)
            db.commit()

    return redirect("/feed")

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
        return redirect("/login")

    sql = """
    DELETE FROM likes
    WHERE user_id=%s AND post_id=%s
    """

    values = (session["user_id"], post_id)

    cursor.execute(sql, values)
    db.commit()

    return redirect("/feed")

@app.route("/comment/<int:post_id>", methods=["POST"])
def comment(post_id):

    if "user_id" not in session:
        return redirect("/login")

    comment_text = request.form["comment"]

    sql = "INSERT INTO comments (comment, user_id, post_id) VALUES (%s, %s, %s)"
    values = (comment_text, session["user_id"], post_id)

    cursor.execute(sql, values)
    db.commit()

    # Get post owner
    sql = """
    SELECT user_id
    FROM posts
    WHERE id=%s
    """

    values = (post_id,)

    cursor.execute(sql, values)

    post_owner = cursor.fetchone()[0]

    # Don't notify yourself
    if post_owner != session["user_id"]:

        notification = f"{session['username']} commented on your post"

        sql = """
        INSERT INTO notifications (user_id, message)
        VALUES (%s, %s)
        """

        values = (post_owner, notification)

        cursor.execute(sql, values)
        db.commit()

    return redirect("/feed")

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

    if request.method == "POST":

        username = request.form["username"]

        sql = "SELECT id, username FROM users WHERE username=%s"
        values = (username,)

        cursor.execute(sql, values)

        user = cursor.fetchone()

        if user:
            return redirect(f"/user/{user[0]}")
        else:
            return "User Not Found"

    return render_template("searchuser.html")

@app.route("/user/<int:user_id>")
def userprofile(user_id):

    sql = """
    SELECT id, username, last_seen
    FROM users
    WHERE id=%s
    """
    values = (user_id,)

    cursor.execute(sql, values)

    user = cursor.fetchone()

    if not user:
        return "User Not Found"

    # User Posts
    sql = """
    SELECT id, content, image
    FROM posts
    WHERE user_id=%s
    ORDER BY id DESC
    """

    values = (user_id,)

    cursor.execute(sql, values)

    posts = cursor.fetchall()

    # Followers Count
    sql = """
    SELECT COUNT(*)
    FROM followers
    WHERE following_id=%s
    """

    values = (user_id,)

    cursor.execute(sql, values)

    followers_count = cursor.fetchone()[0]

    # Following Count
    sql = """
    SELECT COUNT(*)
    FROM followers
    WHERE follower_id=%s
    """

    values = (user_id,)

    cursor.execute(sql, values)

    following_count = cursor.fetchone()[0]

    # Follow Status
    is_following = False

    if "user_id" in session:

        sql = """
        SELECT *
        FROM followers
        WHERE follower_id=%s AND following_id=%s
        """

        values = (session["user_id"], user_id)

        cursor.execute(sql, values)

        follow_record = cursor.fetchone()

        if follow_record:
            is_following = True

    return render_template(
        "userprofile.html",
        user=user,
        posts=posts,
        followers_count=followers_count,
        following_count=following_count,
        is_following=is_following,
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

    sql = """
    INSERT INTO notifications (user_id, message)
    VALUES (%s, %s)
    """

    values = (user_id, notification)

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

@app.route("/followers")
def followers():

    if "user_id" not in session:
        return redirect("/login")

    sql = """
    SELECT users.id, users.username
    FROM followers
    JOIN users
    ON followers.follower_id = users.id
    WHERE followers.following_id=%s
    """

    values = (session["user_id"],)

    cursor.execute(sql, values)

    followers = cursor.fetchall()

    return render_template(
        "followers.html",
        followers=followers
    )

@app.route("/following")
def following():

    if "user_id" not in session:
        return redirect("/login")

    sql = """
    SELECT users.id, users.username
    FROM followers
    JOIN users
    ON followers.following_id = users.id
    WHERE followers.follower_id=%s
    """

    values = (session["user_id"],)

    cursor.execute(sql, values)

    following = cursor.fetchall()

    return render_template(
        "following.html",
        following=following
    )

@app.route("/notifications")
def notifications():

    if "user_id" not in session:
        return redirect("/login")

    sql = """
    SELECT message, created_at
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
        (user_id, message)
        VALUES (%s, %s)
        """

        values = (
        user_id,
        "You received a new message"
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

    sql = """
    SELECT DISTINCT
        users.id,
        users.username
    FROM messages

    JOIN users
    ON messages.sender_id = users.id

    WHERE messages.receiver_id=%s

    ORDER BY users.username
    """

    values = (session["user_id"],)

    cursor.execute(sql, values)

    chats = cursor.fetchall()

    return render_template(
        "inbox.html",
        chats=chats
    )

@app.route("/chat/<int:user_id>")
def chat(user_id):

    if "user_id" not in session:
        return redirect("/login")

    sql = """
    SELECT
        messages.id,
        messages.message,
        users.username,
        messages.sender_id,
        messages.created_at
    FROM messages

    JOIN users
    ON messages.sender_id = users.id

    WHERE
    (messages.sender_id=%s AND messages.receiver_id=%s)
    OR
    (messages.sender_id=%s AND messages.receiver_id=%s)

    ORDER BY messages.id
    """

    values = (
        session["user_id"],
        user_id,
        user_id,
        session["user_id"]
    )

    cursor.execute(sql, values)

    messages = cursor.fetchall()

    return render_template(
        "chat.html",
        messages=messages,
        user_id=user_id
    )

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

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8000)