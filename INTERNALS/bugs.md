## exercise 3. Scaling
1. 
- docker build -t <make-sure-to-give-local-name> .
- the image reference inside replicaset is for local image, not the one inside your dockerhub repository
- so avoid <username>/<image-name> and do just <image-name>

## exercise 4. Docker Networking
1. 
- current version of Flask in requirements.txt is incompatible with Werkzeug version
- put this inside requirements.txt
    Flask==2.2.5
    Werkzeug==2.2.3

2. 
- lightweight images like sqldb, flask-api (ours) and redis might not have ping command (icmp commands) installed
- have to manually install it
- after entering the container terminal using
    > docker exec -it flask-api bash
    install ping by running these commands on the container terminal
        > apt update & apt install iputils-ping -y
        
## exercise 6. Prometheus
1. 
- in `./delivery-monitoring/prometheus.yml` the target for scraping the data needs to be `host.docker.internal:8000` and not `172.17.0.1:8000`. the latter is for linux based systems

2. 
- the command to create a prometheus container needs correction
- [CURRENT_COMMAND]
> docker run -d --name prometheus --network=host -v ./prometheus.yml:/etc/prometheus/prometheus.yml -v ./alert_rules.yml:/etc/prometheus/alert_rules.yml  prom/prometheus
- here --network=host only works on linux based systems
- for windows we need to port map, hence the new command would be:
[CORRECTED_COMMAND]
> docker run -d --name prometheus -p 9090:9090 -v ./prometheus.yml:/etc/prometheus/prometheus.yml -v ./alert_rules.yml:/etc/prometheus/alert_rules.yml  prom/prometheus
