cd /root/parking
git fetch
git merge

cd parking

python3 manage.py migrate --settings=parking.settings_prod
echo yes| python3 manage.py collectstatic --settings=parking.settings_prod

supervisorctl restart parking