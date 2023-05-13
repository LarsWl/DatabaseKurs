sudo apt update
sudo apt install curl build-essential dkms linux-headers-$(uname -r)
### После ДЕЛАЕМ РЕБУТ и ставим VBOX additions чтобы буфер обмана работал)))

# ЧЕЛ НАДО ЩАС ЮЗАТЬ ВПН ЧЕЛ

# =============================================================
# Ставим elasticsearch
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list
sudo apt update
sudo apt install elasticsearch=7.17.0
sudo nano /etc/elasticsearch/elasticsearch.yml
# Раскаментим и меняем
# network.host: localhost

sudo systemctl start elasticsearch
sudo systemctl enable elasticsearch
# Ниже команда для проверки что робiт все
curl -X GET "localhost:9200"

# =============================================================
# Ставим Kibana
sudo apt install kibana=7.17.0
sudo nano /etc/kibana/kibana.yml
# Расскоментим
# elasticsearch.hosts: ["http://localhost:9200"]

sudo systemctl start kibana
sudo systemctl enable kibana
# Чекуем localhost:5601
# Если видеш "Kibana server is not ready yet" - чутка погоди и проверь сервиси service --status-all | grep kibana

# =============================================================
# Ставим Neo4j
sudo apt install python3-pip
pip3 install py2neo
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable 3.5' | sudo tee /etc/apt/sources.list.d/neo4j.list
sudo apt update
sudo apt install neo4j=1:3.5.14

# sudo apt install aptitude
# sudo aptitude install neo4j=1:3.5.14

sudo /usr/bin/neo4j-admin set-initial-password 1234

sudo systemctl start neo4j
sudo systemctl enable neo4j
service --status-all | grep neo4j
# Сразу еще раз меняем паролик
# Пишем cypher-shell, логин и пароль - neo4j
# пишем CALL dbms.changePassword('1234');
# :exit - выходим

# =============================================================
# Ставим Hadoop
sudo addgroup hadoop
sudo adduser --ingroup hadoop hduser
sudo nano /etc/sudoers
# Добавить hduser ALL=(ALL:ALL) ALL
sudo apt-get install openssh-server


sudo su hduser
cd
ssh-keygen -t rsa -P ""
cat $HOME/.ssh/id_rsa.pub >> $HOME/.ssh/authorized_keys

# Качаем худуп
wget https://archive.apache.org/dist/hadoop/core/hadoop-2.9.2/hadoop-2.9.2.tar.gz
sudo tar -xzvf hadoop-2.9.2.tar.gz
sudo mkdir /usr/local/hadoop
sudo mv hadoop-2.9.2 /usr/local/hadoop

sudo mkdir -p /usr/local/hadoop/hadoop_tmp/hdfs/namenode
sudo mkdir -p /usr/local/hadoop/hadoop_tmp/hdfs/datanode
sudo chown hduser:hadoop -R /usr/local/hadoop/

sudo nano .bashrc
# Добавляем строчки:
```
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64
export HADOOP_HOME=/usr/local/hadoop/hadoop-2.9.2
export PATH=$PATH:$HADOOP_HOME/bin
export PATH=$PATH:$HADOOP_HOME/sbin
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"
```

sudo nano /usr/local/hadoop/hadoop-2.9.2/etc/hadoop/hadoop-env.sh
# export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64

sudo nano /usr/local/hadoop/hadoop-2.9.2/etc/hadoop/core-site.xml
# меджду <configuration> и </configuration> добавить
```
<property>
    <name>fs.default.name</name>
    <value>hdfs://localhost:9000</value>
</property>
```

sudo nano /usr/local/hadoop/hadoop-2.9.2/etc/hadoop/hdfs-site.xml
# меджду <configuration> и </configuration> добавить
```
<property>
    <name>dfs.replication</name>
    <value>1</value>
</property>
<property>
    <name>dfs.namenode.name.dir</name>
    <value>file:/usr/local/hadoop/hadoop_tmp/hdfs/namenode</value>
</property>
<property>
    <name>dfs.datanode.data.dir</name>
    <value>file:/usr/local/hadoop/hadoop_tmp/hdfs/datanode</value>
</property>
```

sudo nano /usr/local/hadoop/hadoop-2.9.2/etc/hadoop/yarn-site.xml
# меджду <configuration> и </configuration> добавить
```
<property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
</property>
<property>
    <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
    <value>org.apache.hadoop.mapred.ShuffleHandler</value>
</property>
```

cp /usr/local/hadoop/hadoop-2.9.2/etc/hadoop/mapred-site.xml.template /usr/local/hadoop/hadoop-2.9.2/etc/hadoop/mapred-site.xml
sudo nano /usr/local/hadoop/hadoop-2.9.2/etc/hadoop/mapred-site.xml
# меджду <configuration> и </configuration> добавить
```
<property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
</property>
```

# ВНИМАНИЕ РЕБУТ. ЖДЕМ. МОЖНО ПРИКОЛЬНУТЬСЯ И БЕЗ РЕБУТА, МОЛ, НАХУЯ?
sudo reboot 0

sudo su hduser
hdfs namenode -format

sudo touch hdp.sh
sudo bash -c "echo '/usr/local/hadoop/hadoop-2.9.2/sbin/start-dfs.sh' >> hdp.sh"
sudo bash -c "echo '/usr/local/hadoop/hadoop-2.9.2/sbin/start-yarn.sh' >> hdp.sh"
sudo chmod 777 hdp.sh

sudo touch hdp-stop.sh
sudo bash -c "echo '/usr/local/hadoop/hadoop-2.9.2/sbin/stop-dfs.sh' >> hdp-stop.sh"
sudo bash -c "echo '/usr/local/hadoop/hadoop-2.9.2/sbin/stop-yarn.sh' >> hdp-stop.sh"
sudo chmod 777 hdp-stop.sh

./hdp.sh

# =============================================================
# Ставим Spark (из под hduser)
cd
wget https://archive.apache.org/dist/spark/spark-2.4.6/spark-2.4.6-bin-hadoop2.7.tgz
sudo tar -xzvf spark-2.4.6-bin-hadoop2.7.tgz
mv spark-2.4.6-bin-hadoop2.7 spark-2.4.6
sudo mv spark-2.4.6 /usr/local
sudo chown hduser:hadoop -R /usr/local/spark-2.4.6/
sudo apt install python2
sudo nano .bashrc
# Добавляем вота чо
```
export SPARK_HOME=/usr/local/spark-2.4.6
export PATH=$PATH:$SPARK_HOME/bin
export PYSPARK_PYTHON=/usr/bin/python2
export PYSPARK_DRIVER_PYTHON=python2
```
source .bashrc
spark-shell --version
# Радуемся картинке

cd $SPARK_HOME/conf
sudo cp spark-env.sh.template spark-env.sh
sudo nano spark-env.sh
# Дописываем
```
export SPARK_LOCAL_IP=127.0.0.1
export PYSPARK_PYTHON=/usr/bin/python2
export PYSPARK_DRIVER_PYTHON=python2
```

# ВСЕ

# дополнительно надо кстати вот еще чо
pip install elasticsearch==7.17.0
# А еще добавить в /etc/elasticsearch/elasticsearch.yml строчку
# xpack.security.enabled: false