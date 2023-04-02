from app import create_app
from create_db import create_admin_acct, create_themes, create_dummie_accts, create_posts, create_comments, create_stats, create_likes_and_bookmarks
from app.extensions import db

app = create_app()

with app.app_context():
    db.create_all()
    create_admin_acct()
    create_themes()
    create_stats()
    # the bellow can be deleted, see createdb.py
    create_dummie_accts ()
    create_posts()
    create_comments()
    create_likes_and_bookmarks()

    

if __name__ == '__main__':
    app.run(debug=True)

    