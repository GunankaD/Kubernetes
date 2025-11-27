## EXERCISE 1. HELLO WORLD FOR PODS

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
a. create `app.py` = a simple flask app
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
1. Create small server (`app.py`) and build an image (refer to the Dockerfile for details)
2. Create a `replicaset.yaml` manifest which sets up 3 replicas which use the above image
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
6. remove containers 
    > docker stop flask-api redis sqldb
    > docker rm flask-api redis sqldb

## EXERCISE 5. APPARMOR
1. to secure your containers and not allow anyone to execute binaries or access few of the directories
2. to do this create `app.py` simple flask server that we will be securing. create its own `Dockerfile` and build an image `flask-apparmor`
3. rest of the apparmor profile application will be done in an ubuntu vm
4. create `docker_myprofile` profile and place in /etc/apparmor.d/
    - load the profile
    > sudo apparmor_parser -r /etc/apparmor.d/docker_myprofile
    > sudo aa-enforce docker_myprofile
    > sudo aa-status | grep docker_myprofile
5. test
    > python3 apply_apparmor.py
    > python3 apply_apparmor_test.py


## EXERCISE 6. MONITORING USING PROMETHEUS AND GRAFANA (extra notes in separate .md file)
0. to enter the virtual environment, go exercise6-monitoring folder
    > venv\Scripts\Activate.ps1
    - and run the above command. (this assumes virutal environment was already created)
1. prometheus client
    - A Prometheus client refers to a library or tool that allows an application to expose metrics in a format that the Prometheus monitoring system can scrape and collect.
    - create `delivery_metrics.py` which has 2 types of metrics: guage and summary. 
        - counter: strictly increasing metric
        - guage: is a type of metric that inc or dec
        - histogram: for bar distributions with fixed buckets
        - summary: records the changes too (has history)
    - the script first stirs up a simple server (`start_http_server`)
    - simple server simulates delivery every sec (sleep(1))
    - now access this at http://localhost:8000
2. `prometheus.yml` & `alert_rules.yml`, first one scrapes the data the above prom client gives and second one based on few conditions, throws alert. 
3. run a container with prometheus image, mounted with a volume which contains both the above jobs
    > docker run -d --name prometheus -p 9090:9090 -v ./prometheus.yml:/etc/prometheus/prometheus.yml -v ./alert_rules.yml:/etc/prometheus/alert_rules.yml prom/prometheus

    - -v tag: mounts those 2 jobs in a volume. from local directory to their respective locations inside 
    - prom/prometheus: is the official image
    - now access the running container at http://localhost:9090
    - this scrapes data from http://localhost:8000, go to Status/Target and Query/Graph for insights on the scraped data
4. Grafana
- create a grafana container
> docker run -d --name grafana -p 3000:3000 grafana/grafana
- can access at http://localhost:3000
-  go to connections> add new data source > search prometheus > add location as http://host.docker.internal:9090 > Save and test
- now grafana queries prometheus
- go to dashboard > add new panels > choose any metric (one from the 4 we had created) and display

5. Jenkins
- create a folder `jenkins_home`
> docker run -d --name jenkins `
>>   -p 8080:8080 -p 50000:50000 `
>>   -v "${PWD}\jenkins_home:/var/jenkins_home" `
>>   -v "/var/run/docker.sock:/var/run/docker.sock" `
>>   jenkins/jenkins:lts
- access at http://localhost:8080
- get the password from your jenkins container, run this command
    > docker exec -it jenkins bash
    - once inside the container run
    > cat /var/jenkins_home/secrets/initialAdminPassword
    - this will print the password onto the terminal, copy paste that on jenkins browser
- open and let the plugins install
- install docker in jenkins
    > docker exec -u root -it jenkins bash
    > apt-get update
    > apt-get install -y docker.io
- create a pipeline in jenkins
    - new-item > pipeline > enter github url [https://github.com/GunankaD/Kubernetes/] > under pipelines give Jenkinsfile with scm > enter Jenkinsfile location as [INTERNALS/exercise6-monitoring/delivery-monitoring/Jenkinsfile] > create
    - extra details under Jenkins scm
        - git
        - enter repo url
        - change master to main
        - Jenkinsfile location as `INTERNALS/exercise6-monitoring/delivery-monitoring/Jenkinsfile`
- run the build
- prometheus wont start due to volume mounting issues, start prometheus individually brah ull be fine


## EXERCISE 7. JENKINS
0. pretty basic nothing new
1. command to run a simple lightweight Jenkins container
    > docker run -d --name jenkins -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts
    - port 50000 is for jenkins agents (jenkins main container is called the controller which runs pipelines
    if it automates builds, and if user has seperate agents (other containers) to do this job, then those agents talk to jenkins using the 50k port)
2. access jenkins at http://localhost:8080
3. get jenkins password
    > docker exec -it jenkins bash
    > cat /var/jenkins_home/secrets/initialAdminPassword
    - this should print the pwd out on the terminal, copy paste while logging in


## EXERCISE 8. JENKINS HELLO WORLD JOB
1. create new repo named `devops-sample-code` on github
2. create a fine grained PAT for the above repo and give only `contents` permission (make sure to give read & write persmission)
    - PAT: _check secret.txt for the pat token_
3. install git and docker
    > sudo apt update
    > sudo apt install git
    > sudo apt install docker.io
    > sudo systemctl enable --now docker
    > sudo usermod -aG docker $USERsudo apt install docker
    > sudo reboot
4. follow the steps and push the code
5. follow the steps and start the jenkins
6. create a new item > free style project > enter github url 
    - under build steps select execute shell and add this line
    > sh hello-world.sh
7. To trigger build click on Jenkins Dashboard -> HelloWorld -> Build Now This will trigger the build job.
8. Navigate to the Build History section on the left-hand side of the job page. Click the build number (e.g., #1). Click Console Output to see the build logs.


## EXERCISE 9. 