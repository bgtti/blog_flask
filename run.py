from app import create_app
from create_db import create_admin_acct, create_dummie_accts, create_posts
from app.extensions import db
# from flask import current_app

app = create_app()

with app.app_context():
    db.create_all()
    create_admin_acct()
    create_dummie_accts ()
    create_posts()

    

if __name__ == '__main__':
    app.run(debug=False)

    