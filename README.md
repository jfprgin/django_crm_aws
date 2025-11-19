> A new **serverless version** of this project is available on the [`serverless`](https://github.com/jfprgin/django_crm_aws/tree/serverless) branch.
>
> It uses AWS Lambda, API Gateway, DynamoDB and CDK — see [README.serverless.md](https://github.com/jfprgin/django_crm_aws/blob/serverless/README.serverless.md) for full instructions.

***

# Simple DJango CRUD CRM Application

This project is a simple Django-based CRM application featuring full CRUD (Create, Read, Update, Delete) functionality. It demonstrates how to build a database-driven web application using Django, PostgreSQL, and Bootstrap for styling.

The project includes complete instructions for both local development and production deployment on AWS EC2.
The live server is configured to run behind Gunicorn and Nginx, and is accessible via:

http://13.50.28.85
## Features
- Create new records
- View a list of all records
- Update existing records
- Delete records
- Simple and user-friendly interface

## Tech Stack
- **Backend Framework**: Django (Python)
- **Database**: PostgreSQL
- **Frontend**: Bootstrap (for styling)
- **Environment Management**: Pipenv
- **Server**: Gunicorn + Nginx (for AWS deployment)
- **Version Control**: Git/GitHub

***

## Setup Instructions for Local Development in PyCharm

### 1. Clone the Repository
```bash
git clone <repository_url>
cd django_crm_aws
```

### 2. Setup Python Virtual Environment
Make sure you are in the project root directory and install `pipenv` and activate the virtual environment:

```bash
pipenv shell
```
- You will get something like `/home/<local_user>/.local/share/virtualenvs/django_crm_aws-<random_string>/bin/activate`, save it.

### 3. Install Dependencies
```bash
pipenv install
```

### 4. Configure Python Interpreter in PyCharm
1. Go to **Settings > Python > Interpreter**.
2. Click **Add Interpreter** > **Add Local Interpreter** > **Select Existing**.
3. In  **Browse** paste the `/home/<local_user>/.local/share/virtualenvs/django_crm_aws-<random_string>/bin/activate` and choose `python3.12`:

### 5. Configure Django Settings
1. Go to **Settings > Python > Django**
2. In **"Settings: "** find `settings.py`, and select it.
3. in **"Manage script: "** find `manage.py`, and select it.

### 6. Configure Environment Variables
1. Go to **Run > Edit Configurations** (top right).
2. Under **Environment variables**, set:
   ```
   PYTHONUNBUFFERED=1;DJANGO_SETTINGS_MODULE=core.settings
   
   ```
   
### 7. Database Setup
1. Set up the database (PostgreSQL).
2. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
   
### 8. Running the Development Server
To start the server:
```bash
python manage.py runserver
```

***

## AWS EC2 Deployment Guide
Below is a step-by-step guide for launching and preparing an **EC2 instance** for your **Django CRM AWS** deployment.

### 1. Open the EC2 Dashboard

### 2. Launch a New EC2 Instance

   1. Click _Launch Instance_

![Step 2.1](https://i.ibb.co/1YbG2nSz/Step-1.png)

Once on the _Launch an instance_ page:

   2. Choose a name for the **instance**

![Step 2.2](https://i.ibb.co/qFjY21LD/Step-2-1.png)

   3. Choose an **AMI** (_Ubuntu 24.04 LTS_)

![Step 2.3](https://i.ibb.co/Txb8fSmb/Step-2-2.png)

   4. Choose **Instance Type** (_t3.micro – Free Tier Eligible_)
   - Generating a _Key Pair_ is optional

![Step 2.4](https://i.ibb.co/yFFzPNGM/Step-2-3.png)

   5.1 Configure **Network Settings**
   - Select _Create security group_
   - Allow **SHH** (select _Anywhere 0.0.0.0/0_), **HTTPS** and **HTTP** traffic
   - Click _Edit_ to add aditional **security group rules**

![Step 2.5](https://i.ibb.co/tMvcSM4z/Step-2-4.png)

   5.2 Add the Following **Custom Security Group Rules** (for _Django_ and _PostgreSQL_)

![Step 2.6](https://i.ibb.co/Ld9yKhGV/Step-2-5.png)

   6. _Launch instance_

![Step 2.7](https://i.ibb.co/C57vC6Hy/Step-2-6.png)
   
### 3. Allocate an Elastic IP
This gives your EC2 instance a **static** public IP address.
   1. Under _Network & Security_ find _Elastic IPs_
   2. Click _Allocate Elastic IP address_

![Step 3.1](https://i.ibb.co/CKMk94vt/Step-4-1-1.png)

   3. Associate **Elastic IP** with Your **Instance**

![Step 3.2](https://i.ibb.co/217DSKkW/Step-4-2-1.png)

### 4. View Your Instance Details
- Copy the public IPv4 address and click _Connect_.

![Step 4](https://i.ibb.co/kgBk656x/Step-6.png)

### 5. Connect Using EC2 Instance Connect
- Use the default username _ubuntu_

![Step 5](https://i.ibb.co/Xn57n1K/Step-5-1-1.png)

***

## AWS Server Setup (SSH Console Instructions)

### 1. Configure UFW Firewall
```bash
sudo ufw app list
sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw status
```

### 2. Install System Dependencies
```bash
sudo apt update
sudo apt install python3-pip python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl virtualenv -y
```

### 3. Configure PostgreSQL
```bash
sudo -u postgres psql
```
Inside the PostgreSQL shell:
```sql
CREATE DATABASE django_crm_aws;
CREATE USER admin WITH PASSWORD '<password>';
ALTER ROLE admin SET client_encoding TO 'utf8';
ALTER ROLE admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE admin SET timezone TO 'CET';
GRANT ALL PRIVILEGES ON DATABASE django_crm_aws TO admin;
\q
```

### 4. Create and Activate Virtual Environment
```bash
python3 -m venv env
pip install django gunicorn
```
Install Pipenv:
```bash
sudo apt install pipenv
pipenv install
```

### 5. Run Django Migrations and Create Admin User
```bash
python3 manage.py migrate
python3 manage.py createsuperuser
```

### 6. Allow Django Development Port (Optional)
```bash
sudo ufw allow 8000
```
Run Django dev server:
```bash
python3 manage.py runserver 0.0.0.0:8000
```

## Configure Gunicorn (Production WSGI Server)
### 7. Create Gunicorn Socket
```bash
sudo nano /etc/systemd/system/gunicorn.socket
```
Paste:
```ini
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=socket.target
```

### 8. Create Gunicorn Service
```bash
sudo nano /etc/systemd/system/gunicorn.service
```
Paste:
```ini
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/django_crm_aws
ExecStart=/home/ubuntu/django_crm_aws/env/bin/gunicorn \
        --access-logfile - \
        --workers 3 \
        --bind unix:/run/gunicorn.sock \
        core.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 9. Start and Enable Gunicorn
```bash
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
file /run/gunicorn.sock
sudo systemctl status gunicorn
curl --unix-socket /run/gunicorn.sock localhost
```

## Configure Nginx Reverse Proxy
### 10. Create Nginx Site Configuration
```bash
sudo nano /etc/nginx/sites-available/django_crm_aws
```
Paste:
```nginx
server {
        listen 80;
        server_name 13.50.28.85;

        location = /favicon.ico { access_log off; log_not_found off; }
        location /static/ {
                alias /home/ubuntu/django_crm_aws/staticfiles/;
        }

        location / {
                include proxy_params;
                proxy_pass http://unix:/run/gunicorn.sock;
        }
}
```
Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/django_crm_aws /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

## 11. Update Firewall for Nginx
```bash
sudo ufw delete allow 8000
sudo ufw allow 'Nginx Full'
```

## 12. Update Nginx User (To fix admin panel styling)
```bash
sudo nano /etc/nginx/nginx.conf
```
Change:
```bash
user www-data;
```
to:
```bash
user ubuntu;
```
Then:
```bash
sudo systemctl restart nginx
```

***

## Contact
If you have any questions or suggestions, feel free to reach out to:
- **Email**: jfprgin@gmail.com
