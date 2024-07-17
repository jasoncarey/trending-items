# MACOS Usage

## Start Script

`python3 scripts/start.py`

## Alternatively

### MongoDB

`brew services start mongodb-community@7.0` - start MongoDB as MacOs service
`brew services list` - view running services

### Zookeeper

Apache Kafka requires Zookeeper to be running for cluster management
`/opt/homebrew/bin/zookeeper-server-start /opt/homebrew/etc/zookeeper/zoo.cfg`

### Kafka

`/opt/homebrew/bin/kafka-server-start /opt/homebrew/etc/kafka/server.properties`
`kafka-topics --list --bootstrap-server localhost:9092` - view topics
`kafka-console-consumer --bootstrap-server localhost:9092 --topic interactions --from-beginning` - view messages in topic

## Notes

- MongoDB stores items in BSON (binary representation of JSON)
