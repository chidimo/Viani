steel #0A1612
denim #1A2930
screen #C5C1C0
navy blue #0F1626
eggshell #F5F5F5
leather #AB987A
stormy #494E6B
sunset #985E6D

pipenv install django==2.1.7 pygments==2.3.1 sorl-thumbnail==12.5.0 django-pure-pagination==0.3.0 django-addanother==2.0.0 python-decouple==3.1 rules==2.0.1 django-extensions==2.1.5 psycopg2==2.7.7 requests==2.21.0 pillow==5.4.1 raven==6.10.0 mysqlclient==1.4.2 whitenoise==4.1.2

mysqldump -u vianifashion -h vianifashion.mysql.pythonanywhere-services.com 'vianifashion$viani'  > viani.sql
mysql -u vianifashion -h vianifashion.mysql.pythonanywhere-services.com 'vianifashion$vianirestore'  < viani.sql

'psql -h localhost -d viani -U postgres -f viani.sql';

python manage.py createperms
python manage.py cleanperms
python manage.py grantperms
