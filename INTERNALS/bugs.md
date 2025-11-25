## exercise 3
1. 
- docker build -t <make-sure-to-give-local-name> .
- the image reference inside replicaset is for local image, not the one inside your dockerhub repository
- so avoid <username>/<image-name> and do just <image-name>

## exercise 4
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
        
