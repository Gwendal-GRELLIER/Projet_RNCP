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