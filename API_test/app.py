# app.py
# Main application file for the API Testing & Monitoring Dashboard.
# Final corrected version for database commits.

import sqlite3
import requests
import time
import json
from flask import Flask, render_template, request, redirect, url_for, g, jsonify, abort, flash
import click

# --- Application Setup ---
app = Flask(__name__)
app.config['DATABASE'] = 'api_monitor.db'
app.config['SECRET_KEY'] = '9f1b8c7e3a5f46f2d1c75e0a2b8d64ff0e28c5c7d9f2d43b1b7e9c8f92a4e1d2'


# --- Database Helper Functions ---

def get_db():
    """Establishes a connection to the SQLite database."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Closes the database connection at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Initializes the database using the schema.sql file."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('init-db')
def init_db_command():
    """Creates the database tables."""
    with app.app_context():
        init_db()
    click.echo('Initialized the database.')

# --- Core Logic ---

def run_api_test(endpoint_id):
    """
    Performs an HTTP request to a given endpoint and records the result.
    This function now operates within the app context to ensure DB commits work.
    """
    with app.app_context():
        db = get_db()
        endpoint = db.execute('SELECT * FROM endpoints WHERE id = ?', (endpoint_id,)).fetchone()

        if not endpoint:
            return None

        url, method = endpoint['url'], endpoint['method']
        headers = json.loads(endpoint['headers']) if endpoint['headers'] else {}
        body = json.loads(endpoint['body']) if endpoint['body'] else {}
        
        status_code, response_time, response_body, error_message, is_success = 0, 0, "", "", False

        try:
            start_time = time.time()
            response = requests.request(method, url, json=body, headers=headers, timeout=10)
            response_time = round((time.time() - start_time) * 1000)
            status_code = response.status_code
            response_body = response.text
            is_success = (status_code == endpoint['expected_status'])
        except requests.exceptions.RequestException as e:
            error_message = str(e)

        db.execute(
            'INSERT INTO history (endpoint_id, status_code, response_time, response_body, is_success, error_message) VALUES (?, ?, ?, ?, ?, ?)',
            (endpoint_id, status_code, response_time, response_body, is_success, error_message)
        )
        db.commit()
        return True

# --- Web Page Routes ---

@app.route('/')
def dashboard():
    db = get_db()
    query = """
    SELECT 
        e.id, e.name, e.url, e.method,
        h.is_success, h.status_code, h.response_time, h.checked_at
    FROM endpoints e
    LEFT JOIN (
        SELECT *, ROW_NUMBER() OVER(PARTITION BY endpoint_id ORDER BY checked_at DESC) as rn
        FROM history
    ) h ON e.id = h.endpoint_id AND h.rn = 1
    ORDER BY e.name;
    """
    endpoints = db.execute(query).fetchall()
    return render_template('dashboard.html', endpoints=endpoints)

@app.route('/endpoint/add', methods=['GET', 'POST'])
def add_endpoint():
    if request.method == 'POST':
        db = get_db()
        db.execute(
            'INSERT INTO endpoints (name, url, method, headers, body, expected_status) VALUES (?, ?, ?, ?, ?, ?)',
            [
                request.form['name'], request.form['url'], request.form['method'],
                request.form['headers'] or '{}', request.form['body'] or '{}',
                int(request.form['expected_status'])
            ]
        )
        db.commit()
        flash(f"Endpoint '{request.form['name']}' was successfully added.", 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_endpoint.html')

@app.route('/endpoint/<int:endpoint_id>')
def endpoint_details(endpoint_id):
    db = get_db()
    endpoint = db.execute('SELECT * FROM endpoints WHERE id = ?', (endpoint_id,)).fetchone()
    if not endpoint: abort(404)
    history = db.execute('SELECT * FROM history WHERE endpoint_id = ? ORDER BY checked_at DESC', (endpoint_id,)).fetchall()
    return render_template('endpoint_details.html', endpoint=endpoint, history=history)

@app.route('/endpoint/test/<int:endpoint_id>', methods=['POST'])
def test_endpoint(endpoint_id):
    run_api_test(endpoint_id)
    flash('API test has been executed. See the result below.', 'info')
    return redirect(url_for('endpoint_details', endpoint_id=endpoint_id))

@app.route('/endpoint/delete/<int:endpoint_id>', methods=['POST'])
def delete_endpoint(endpoint_id):
    db = get_db()
    db.execute('DELETE FROM history WHERE endpoint_id = ?', (endpoint_id,))
    db.execute('DELETE FROM endpoints WHERE id = ?', (endpoint_id,))
    db.commit()
    flash('Endpoint and its history have been deleted.', 'success')
    return redirect(url_for('dashboard'))
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
