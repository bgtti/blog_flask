from flask import Flask, render_template
from posts import the_posts
from themes import the_themes

app = Flask(__name__)


@app.route("/")
def home():
    posts_all = the_posts
    for post in posts_all:
        post.update(
            {"picture_big": f"../static/{post['picture_big']}",
            "picture_small": f"../static/{post['picture_small']}"}
        )
    posts_themes = [[post["theme"], f"../static/{post['picture']}"] for post in the_themes]
    print(posts_themes)
    return render_template('index.html', posts_all=posts_all, posts_themes=posts_themes)

if __name__ == "__main__":
    app.run(debug=True)
