from flask import Flask, render_template
from posts import the_posts
from themes import the_themes
from authors import the_authors
import copy

app = Flask(__name__)


@app.route("/")
def home():
    posts_all = copy.deepcopy(the_posts)
    for post in posts_all:
        post.update(
            {"picture_big": f"../static/{post['picture_big']}",
            "picture_small": f"../static/{post['picture_small']}"}
        )
    posts_themes = [[post["theme"], f"../static/{post['picture']}"] for post in the_themes]
    return render_template('index.html', posts_all=posts_all, posts_themes=posts_themes)


@app.route("/all/")
def all():
    posts_all = copy.deepcopy(the_posts)
    for post in posts_all:
        intro = f"{post['intro'][:300]}..."
        post.update(
            {"picture_big": f"../static/{post['picture_big']}",
             "picture_small": f"../static/{post['picture_small']}",
             "intro": intro}
        )
    return render_template('all_posts.html', posts_all=posts_all)

@app.route("/about/")
def about():
    authors_all = copy.deepcopy(the_authors)
    for author in authors_all:
        author.update(
            {"picture": f"../static/{author['picture']}",
        })
    return render_template('about.html', authors_all=authors_all)


if __name__ == "__main__":
    app.run(debug=True)
