# Import necessary modules
import os
import os.path as op
import json
from flask import Flask, jsonify, render_template, abort
from flask_sqlalchemy import SQLAlchemy
import flask_admin as admin
from flask_admin.contrib.sqla import ModelView

# Create Flask application
app = Flask(__name__)

# Configuration settings (consider using environment variables)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'
app.config['FLASK_ADMIN_SWATCH'] = 'flatly'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:changeme@db/flask'
app.config['SQLALCHEMY_ECHO'] = True

# Initialize SQLAlchemy for database management
db = SQLAlchemy(app)

# Define the Hosts database model
class Hosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.Unicode(64), unique=True)
    operating_system = db.Column(db.Unicode(64))
    platform = db.Column(db.Unicode(64))
    created_at = db.Column(db.Unicode(64))
    project_name = db.Column(db.Unicode(80))
    ip = db.Column(db.Unicode(64))
    proc = db.Column(db.Unicode(64))
    memory = db.Column(db.Unicode(64))
    arch = db.Column(db.Unicode(64))

# Create a custom admin view
class CustomView(ModelView):
    pass

class HostsAdmin(CustomView):
    column_searchable_list = ('hostname', 'ip', 'project_name')
    column_filters = ('platform', 'project_name', 'operating_system')
    can_export = True
    export_types = ['csv', 'xlsx']
    can_view_details = True

# Define application routes
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'

# Create admin interface with custom base template
admin = admin.Admin(app, 'Servers', template_mode='bootstrap4')

# Add views
admin.add_view(HostsAdmin(Hosts, db.session))

# Initialize the database (consider using migrations in production)
def initialize_db():
    with app.app_context():
        db.create_all()

# Route to return host list from the database as JSON
@app.route('/api/v1.0/hosts', methods=['GET'])
def get_hosts():
    if os.path.isfile('/tmp/update.lock'):
        return jsonify({'message': 'Update is running'}), 423

    hosts = Hosts.query.all()
    host_data_list = []

    for host in hosts:
        host_data = {
            'hostname': host.hostname,
            'operating_system': host.operating_system,
            'platform': host.platform,
            'created_at': host.created_at,
            'project_name': host.project_name,
            'ip': host.ip,
            'proc': host.proc,
            'memory': host.memory,
            'arch': host.arch
        }
        host_data_list.append(host_data)

    return jsonify(host_data_list)

@app.route('/generate_prom', methods=['GET'])
# Render a template for Prometheus job configuration
def render_template_prometheus_job(infra, hosts):
   for host in hosts:
        redefine_environment(host)
        redefine_group(host)
    # sort list by environment
    hosts = sorted(hosts, key=lambda host: host.env)
    return render_template('hosts.jinja2', infra=infra, hosts=hosts)

if __name__ == '__main__':
    # Remove lock file if it exists (consider using a more robust locking mechanism
    
    # Initialize the database (for development purposes, use migrations in production)
    initialize_db()
    
    # Start the Flask application
    app.run(debug=True, host="0.0.0.0")