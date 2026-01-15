# Hosting project on the linux server (Tested on Ubuntu)

**Creating a service for your Django project ensures that it runs continuously in the background, even after a reboot. You can achieve this by setting up a systemd service on a Linux system. Here's how to do it step by step:**

### Step 1: Prepare Your Django Project

Activate the Virtual Environment:

    cd /path/to/your/django/project
    source /path/to/your/venv/bin/activate

Test the Server: Ensure your project runs properly with:

    python manage.py runserver 0.0.0.0:5000

\*NB: sometimes you need to run all python related commands starting with **_pipenv run_** to make sure they run in virtual environment: \*for example\*\*

    pipenv run python manage.py runserver 0.0.0.0:8000

If everything works, proceed to set up the service.

### Step 2: Create a Gunicorn Configuration (Optional but Recommended)

Using Gunicorn as the application server is more efficient than Django's development server.

Install Gunicorn:

    pip install gunicorn

Test Gunicorn:

    gunicorn --workers 3 --bind 0.0.0.0:8000 vm_is_backend.wsgi

for the case of this project it could be

    gunicorn --workers 3 --bind 0.0.0.0:8000 vm_is_backend.wsgi

Replace myproject.wsgi with the correct path to your wsgi.py module.

### Step 3: Create a Systemd Service File

Open a new service file for editing:

    sudo nano /etc/systemd/system/vilcom_service.service
    sudo nano /etc/systemd/system/ilmis-conversion.service


Add the following content to the file:
<!--  -->
[Unit]
Description=Vilcom daemon
After=network.target

[Service]
User=allan
Group=allan
WorkingDirectory=/home/vilcom/vilcom_project/Vilcom-digital-Restaurant
ExecStart=/home/vilcom/vilcom_project/Vilcom-digital-Restaurant/vilcomVenv/bin/gunicorn --workers 3 --bind unix:/home/vilcom/vilcom_project/Vilcom-digital-Restaurant/vilcom.sock vm_is_backend.wsgi:application

[Install]
WantedBy=multi-user.target
<!--  -->

vilcomVenv
### Step 4: Reload Systemd and Enable the Service

Reload systemd to recognize the new service:

    sudo systemctl daemon-reload

Start the service:

    sudo systemctl start vilcom_service

Enable the service to start on boot:

    sudo systemctl enable vilcom_service
    sudo systemctl restart vilcom_service

### Step 5: Check the Service Status

Check if the service is running:

    sudo systemctl status vilcom_service
    sudo systemctl restart vilcom_service


You should see the service's status as active (running).

### Step 6: Set Up Nginx (Optional for Production)

Using Nginx as a reverse proxy can help serve static files and handle requests more efficiently.

Install Nginx (if not installed):

    sudo apt install nginx

Create an Nginx configuration for your project:

    sudo nano /etc/nginx/sites-available/vilcom.conf
    sudo nano /etc/nginx/sites-available/ilmis.conf

Add the following content:

Enable the Nginx configuration:
    sudo ln -s /etc/nginx/sites-available/vilcom.conf /etc/nginx/sites-enabled
    sudo systemctl restart nginx

Your Django project should now run as a service and restart automatically if the server is rebooted.

check nginx if has no error in configuration

Add this to the below
sudo nano /etc/nginx/nginx.conf
<!--  -->
  server {
        listen       8000;
        listen       [::]:8000;
        server_name  _;
        root         /usr/share/nginx/html;

        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

        error_page 404 /404.html;
        location = /404.html {
        }

        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
        }
    }

<!-- 
sudo nano /etc/nginx/nginx.conf
 -->

<!-- loading statics file css -->
python manage.py collectstatic
<!--  -->



# Ardhi!2024 password ya server ya 35 
# Ardhi!2023 live .20

# password for user postgres .35
# Ardhi@2025


# CREATE DATABASE vilcom_db ;
# CREATE USER vilcom ;
# GRANT ALL privileges on vilcom_db to  vilcom ;

# vilcom ip = 82.25.119.147
# vilcom server public
# username:root
# password:Vilcomtz@2025

# Vilcom user Credations
# username:vilcom
# password:Vilcomuser@2025

# CREATE USER vilcom WITH PASSWORD 'vilcom@2023';
# ALTER ROLE vilcom SET client_encoding TO 'utf8';
# ALTER ROLE vilcom SET default_transaction_isolation TO 'read committed';
# ALTER ROLE vilcom SET timezone TO 'UTC';


# GRANT ALL PRIVILEGES ON DATABASE vilcom_db TO vilcom;
<!-- GRANT ALL PRIVILEGES ON DATABASE vm_is_db TO  vm_is_user ; -->

# python3 -m venv vilcomVenv
# sudo nano /vilcom_backen/settings.py
# ssh vilcom@82.25.119.147

# GRANT ALL ON SCHEMA public TO vm_is_user ;
# GRANT ALL PRIVILEGES ON SCHEMA public TO vm_is_user;
# ALTER SCHEMA public OWNER TO vm_is_user;
# GRANT ALL PRIVILEGES ON SCHEMA public TO vm_is_user;
# SELECT grantee, privilege_type FROM information_schema.role_schema_grants WHERE schema_name = 'public' AND grantee = 'vm_is_user' ;


