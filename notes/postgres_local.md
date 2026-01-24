open pgAdmin4


https://gist.github.com/Kartones/dd3ff5ec5ea238d4c546


command line login
which psql

"postgres://maggie:[passwd]@host.docker.internal:5432/web_dev"
erase database
create a bare database
sudo -u postgres psql
\l
\du
DROP DATABASE web_dev
DROP DATABASE web_test
CREATE DATABASE web_dev
GRANT ALL PRIVILEGES ON DATABASE web_dev TO maggie

psql -U maggie -h localhost -d web_dev
\dt
make sure DATABASE_URL is correctly set in the secrets file 
postgres://maggie:[passwd]@host.docker.internal:5432/web_dev

start docker containers and run tests

https://testdriven.io/courses/tdd-fastapi/postgres-setup/
Do tables get created automatically?
register_tortoise create_schemas is true

not working
psql -U maggie -h host.docker.internal -d web_dev

test host.docker.internal
curl http://localhost:80
curl http://host.docker.internal:80 test this out

edit postgresql.conf
listen_addresses = '*'

edit pg_hba.conf
host all all 0.0.0.0/0 md5

select auth_sub from "user";
select * from "user";
You need quotes because user is a reserved key name.
https://stackoverflow.com/questions/22256124/cannot-create-a-database-table-named-user-in-postgresql


