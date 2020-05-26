zookeeper-shell.sh localhost:2181 <<EOF
ls /brokers/topics
deleteall /brokers/topics/test-1
deleteall /brokers/topics/benchmark-1-1-none
ls /brokers/topics
quit
EOF
