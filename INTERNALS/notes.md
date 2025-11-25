## EXERCISE 1

1. Setup
- minikube start 
- doskey k=kubectl $*

2. Running one single pod
- k run <pod-name> --image=<image-name> --port=<port-no.>
- ex: k run hello-k8s --image=nginx --port=80

3. Creating external service so that the pod can be accessed from browser
- k expose pod <pod-name> --type=<type> --port=<port-no.>
- k expose pod hello-k8s --type=NodePort --port=80
- It creates a Service object so your pod can be reached from outside.
    1. expose = make a Service for an existing Pod
    2. pod hello-k8s = expose this specific pod
    3. --type=NodePort = open a port on the node (e.g., 30000–32767)
    4. --port=80 = service will forward traffic to port 80 inside the pod

4. To access the service
- minikube service <service-name>
- ex: minikube service hello-k8s
- here the service name is same as the pod name

D:\IMPORTANT\Projects\Kubernetes\internals\exercise1-hello-pod>minikube service hello-k8s
|-----------|-----------|-------------|---------------------------|
| NAMESPACE |   NAME    | TARGET PORT |            URL            |
|-----------|-----------|-------------|---------------------------|
| default   | hello-k8s |          80 | http://192.168.49.2:31735 |
|-----------|-----------|-------------|---------------------------|
🏃  Starting tunnel for service hello-k8s.
|-----------|-----------|-------------|------------------------|
| NAMESPACE |   NAME    | TARGET PORT |          URL           |
|-----------|-----------|-------------|------------------------|
| default   | hello-k8s |             | http://127.0.0.1:59517 |
|-----------|-----------|-------------|------------------------|
🎉  Opening service default/hello-k8s in default browser...
❗  Because you are using a Docker driver on windows, the terminal needs to be open to run it.


## EXERCISE 2. CREATE AND DEPLOY A FLASK APP IN A CONTAINER IN KUBERNETES
1. Create an image
a. create app.py = a simple flask app
b. create Dockerfile
c. cd to current folder
d. configure docker to build images inside minikube
    > minikube docker-env 
    - then run the last command in the output
c. > docker build -t <image-name> .
    ex: docker build -t flask-app .
e. confirm image
    -

2. Create a deployment which uses the above created image
- keep the imagePullPolicy=NEVER, it only uses the local one if exists and doesnt search on dockerhub
- create the deployment yaml
    > k apply -f flask-deployment.yaml

3. Call minikube to create a tunnel and expose service from browser
    > minikube service flask-service

## EXERCISE 3. SCALING PODS USING REPLICASET
1. Create small server (app.py) and build an image (refer to the Dockerfile for details)
2. Create a 'replicaset.yaml' manifest which sets up 3 replicas which use the above image
    - also setup the liveness probe and readyness probe
3. apply -f replicaset.yaml and then check if everything working
4. > minikube service flashsale-svc # this starts up the terminal
5. scale up the number of replicas
    > k scale replicaset flashsale-rs --replicas=5

## EXERCISE 4. NETWORKING USING BRIDGE NETWORK
1. 3 containers: flask app, sql db, redis
2. create a bridge network inside the docker
    > docker network create --driver=bridge my-bridge-net
3. create a small flask server and build an image (refer to the Dockerfile for details)
    > docker build -t flask-api .
4. spawn 3 containers, while the flask container uses the image we just created
    docker run -d --name mysql --net=my-bridge-net mysql:latest
    docker run -d --name redis --net=my-bridge-net redis:latest
    docker run -d --name flask --net=my-bridge-net -p 5001:5001 flask-api
5. exec into any of the container and ping the others
    > docker exec -it flask-api bash
    - i in it stands for interactive (sends your keyboard input)
    - t displays terminal
    - light weight images wont have ping command
        > apt update
        > apt install iputils-ping -y
    - this will install ping and now available to use!
    > ping redis

## EXERCISE 5.
 