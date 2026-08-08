git clone https://github.com/zhgoodnight-bit/Modul19-Assignment

cd Modul19-Assignment
cd banking-system

# Windows
.\my_env\Scripts\activate

# Linux/Mac
source .\my_env\Scripts\activate

pip install -r requirements.txt

cd .\banking_system\ 
python manage.py migrate

python manage.py createsuperuser

python manage.py runserver

hit: http://127.0.0.1:8000/dashboard/