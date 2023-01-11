import sqlite3
import logging
import sys
from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

db_connection_count = 0
# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    #global db_connection_count
    db_connection_count += 1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Function to get total number of posts in the database
def get_posts_count():
    connection = get_db_connection()
    posts_count = connection.execute('SELECT COUNT(*) FROM posts').fetchone()
    connection.close()
    return posts_count

# Function to get total number of connections to the database
def get_db_connection_count():
    #global db_connection_count
    return db_connection_count

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.error('Non-existing article with id ' + post_id + ' requested!')
      return render_template('404.html'), 404
    else:
      app.logger.info('Article ' + post['title'] + ' record retrieved!')
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()

            ## log line
            app.logger.info('Article ' + title + ' record created!')

            return redirect(url_for('index'))

    return render_template('create.html')


# Define the Healthcheck endpoint
@app.route('/healthz')
def health_status():
    response = app.response_class(
        response = json.dumps({"result":"OK - healthy"}),
        status   = 200,
        mimetype = 'application/json'
    )
    ## log line
    app.logger.info('Heathcheck request successfull')
    return response


# Define the Metrics endpoint
@app.route('/metrics')
def metrics():
    response = app.response_class(
          response = json.dumps({
            "status":"success",
            "code"  : 0,
            "data"  : { "post_count"          : get_posts_count(),
                        "db_connection_count" : get_db_connection_count()}}),
          status   = 200,
          mimetype ='application/json'
    )
    ## log line
    app.logger.info('Metrics request successfull')
    return response


# start the application on port 3111
if __name__ == "__main__":
    stdout_hdlr = logging.StreamHandler(stream=sys.stdout)
    stderr_hdlr = logging.StreamHandler(stream=sys.stderr)

    ## stream logs to app.log file
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[stdout_hdlr, stderr_hdlr],
        format='%(levelname)s:%(name)s, %(asctime)s, %(message)s')

    app.run(host='0.0.0.0', port='3111')
