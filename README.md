
# clone project with the help of git link
git clone https://github.com/Diman2003/vendor_management.git

# create and activate virtual environment in Linux
python3 -m venv env
source env/bin/activate

# create and activate virtual environment in Window'cmd
python -m venv env
cd env/Scripts
activate

# install required libraries and tools
pip install -r requirements.txt

# Apply Migrations
python3 manage.py makemigrations
python3 manage.py migrate

# Run Project
python3 manage.py runserver


# Admin Id Pass
user: vendor
pass : 123456

# Or Create new superuser
python3 manage.py createsuperuser


# =========================
use can user postmen collection to use APIViews