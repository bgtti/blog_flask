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
    posts_themes = [
        [post["theme"], f"../static/{post['picture']}", post["id"]] for post in the_themes]
    return render_template('index.html', posts_all=posts_all, posts_themes=posts_themes)

@app.route("/all/<int:index>")
def all(index):
    all_blog_posts = []
    chosen_theme = ""
    if index != 0:
        for theme in the_themes:
            if theme["id"] == index:
                chosen_theme = theme["theme"]

    for post in the_posts:

        if index != 0 and post["theme"] != chosen_theme:
            continue
        else:
            post_at_hand = dict(post)
            intro = f"{post_at_hand['intro'][:300]}..."
            post_at_hand.update(
                {"picture_big": f"../static/{post_at_hand['picture_big']}",
                "picture_small": f"../static/{post_at_hand['picture_small']}",
                "intro": intro}
            )
            all_blog_posts.append(post_at_hand)
    
    return render_template('all_posts.html', all_blog_posts=all_blog_posts, chosen_theme=chosen_theme)

@app.route("/about/")
def about():
    authors_all = copy.deepcopy(the_authors)
    for author in authors_all:
        author.update(
            {"picture": f"../static/{author['picture']}",
        })
    return render_template('about.html', authors_all=authors_all)


@app.route("/post/<int:index>")
def blog_post(index):
    blog_posts = copy.deepcopy(the_posts)
    post_author = None
    for post in blog_posts:
        if post["id"] == index:
            blog_posts = post
            blog_posts.update(
                {"picture_big": f"../static/{post['picture_big']}",
                "picture_small": f"../static/{post['picture_small']}"})
            for author in the_authors:
                if author["name"] == post["author"]:
                    post_author = dict(author)
                    post_author.update({
                        "picture": f"../static/{author['picture']}"
                    })

    return render_template('post.html', blog_posts=blog_posts, post_author=post_author)


if __name__ == "__main__":
    app.run(debug=True)
