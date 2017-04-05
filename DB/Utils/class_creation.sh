mysql -u $1 -p < ../quizzDB.sql
python -m pip install peewee
python pwiz.py -u $1 -P --engine=mysql $2 > classes.py

