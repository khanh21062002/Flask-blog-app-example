from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from auth import login_required
from db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN users u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    )
    posts = cursor.fetchall()
    cursor.close()
    return render_template('blog/index.html', posts=posts)
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (%s, %s, %s)',
                (title, body, g.user['id'])
            )
            db.commit()
            cursor.close()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')
def get_post(id, check_author=True):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN users u ON p.author_id = u.id'
        ' WHERE p.id = %s',
        (id,)
    )
    post = cursor.fetchone()  # Lấy kết quả của truy vấn
    cursor.close()  # Đóng con trỏ sau khi sử dụng

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")# Kiểm tra nếu không có bài viết

    if check_author and post['author_id'] != g.user['id']: # Kiểm tra author_id
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                'UPDATE post SET title = %s, body = %s'
                ' WHERE id = %s',
                (title, body, id)
            )
            db.commit()
            cursor.close()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM post WHERE id = %s', (id,))
    db.commit()
    cursor.close()
    return redirect(url_for('blog.index'))