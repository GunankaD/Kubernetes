# 1. Starting and Stopping Minikube
minikube start                            # Start Minikube with default settings
minikube start --kubernetes-version=v1.21.2  # Start with a specific Kubernetes version
minikube stop                             # Stop Minikube without deleting
minikube delete                           # Delete Minikube cluster

# 2. Checking Status and Information
minikube status                           # Check Minikube status
kubectl cluster-info                      # Display cluster information

# 3. Accessing Services
minikube service <service-name>           # Open specified service in browser
minikube service list                     # List URLs of all services
minikube tunnel                           # Create a network tunnel to access LoadBalancer services

# 4. Docker with Minikube
eval $(minikube docker-env)               # Use Minikube's Docker daemon
docker build -t my-image .                # Build image directly in Minikube
minikube image load my-image              # Load a local image into Minikube

# 5. Debugging and Logs
minikube logs                             # View Minikube logs
minikube dashboard                        # Open the Kubernetes dashboard
minikube ssh                              # SSH into the Minikube VM