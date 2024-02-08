# Projet_RNCP

pip install kaggle
mv /workspaces/Projet_RNCP/kaggle.json /home/codespace/.kaggle

kaggle competitions download -c open-problems-single-cell-perturbations

unzip /workspaces/Projet_RNCP/open-problems-single-cell-perturbations.zip

python -m venv env 

source env/bin/activate


docker-compose up -d

docker exec -it kafka /bin/sh
cd /opt/kafka_2.13-2.8.1/bin
kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic file-stream



docker :

@Gwendal-GRELLIER ➜ /workspaces/Projet_RNCP (Flask) $ docker network ls
NETWORK ID     NAME                     DRIVER    SCOPE
390c492497b0   bridge                   bridge    local
79839b6d84b3   host                     host      local
a9a1f000334b   ml_flow_server_default   bridge    local
72bf6958db46   none                     null      local
c3d4a90219aa   thor                     bridge    local
@Gwendal-GRELLIER ➜ /workspaces/Projet_RNCP (Flask) $ docker network create ml_flow
4d1d28a817698f2448216b6ec72cc2aff7dfce16da0aefda84c73a1410b34fb4
@Gwendal-GRELLIER ➜ /workspaces/Projet_RNCP (Flask) $ docker run -d --network ml_flow --network-alias mysql -v mysql-data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=ml-flow-data mysql:5.7 
d4491358140f47b5708272034a885f12907ec4e075d7d298b84b6afcfc7f69e7
@Gwendal-GRELLIER ➜ /workspaces/Projet_RNCP (Flask) $ docker exec -it d4491358140f47b5708272034a885f12907ec4e075d7d298b84b6afcfc7f69e7  mysql -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 2
Server version: 5.7.44 MySQL Community Server (GPL)

Copyright (c) 2000, 2023, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| ml-flow-data       |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.01 sec)

mysql> exit
Bye

docker-compose down
docker rmi -f $(docker images -q)
docker-compose build
docker-compose compose up -d