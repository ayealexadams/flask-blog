# flask-blog

[![CircleCI](https://circleci.com/gh/ayealexadams/flask-blog/tree/master.svg?style=svg)](https://circleci.com/gh/ayealexadams/flask-blog/tree/master)

A blogging website built on the Flask micro framework.

# Environment Variables

You will need the following system environment variables to run this website.

`FLASK_BLOG_SECRET
FLASK_BLOG_DB_URL
FLASK_BLOG_EMAIL_USERNAME
FLASK_BLOG_EMAIL_PASSWORD`

# Database

If it is your first time running the website you will need to create a new database.

`from blog import db
db.create_all()`
