# Kubernetes Hands-On Project

A comprehensive full-stack ToDo application deployed on Kubernetes (minikube) demonstrating advanced Kubernetes features including ConfigMap, Secret, Ingress, HPA (Horizontal Pod Autoscaler), and monitoring with Kubernetes Dashboard.

## Project Overview

- **Backend**: Flask REST API (Python)
- **Frontend**: Vanilla JavaScript, HTML, CSS
- **Database**: SQLite
- **Containerization**: Docker
- **Orchestration**: Kubernetes (minikube)
- **Features**: ConfigMap, Secret, Ingress, HPA, Health Checks, Resource Limits

## Project Structure

```
.
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker image definition
├── static/               # Frontend files
│   ├── index.html
│   ├── style.css
│   └── app.js
├── k8s/                  # Kubernetes manifests
│   ├── configmap.yaml    # Application configuration
│   ├── secret.yaml       # Sensitive data
│   ├── deployment.yaml   # Application deployment
│   ├── service.yaml      # ClusterIP service
│   ├── ingress.yaml      # Ingress controller
│   └── hpa.yaml          # Horizontal Pod Autoscaler
└── README.md
```

## Technologies Used

- **Flask**: Python web framework
- **SQLite**: Lightweight database
- **Docker**: Containerization
- **Kubernetes**: Container orchestration
- **minikube**: Local Kubernetes cluster
- **NGINX Ingress**: Ingress controller
- **HPA**: Horizontal Pod Autoscaler
- **Kubernetes Dashboard**: Web UI for cluster management

## Advanced Features Demonstrated

1. **ConfigMap**: Configuration management
2. **Secret**: Sensitive data management
3. **Ingress**: External access and routing
4. **HPA**: Automatic scaling based on metrics
5. **Health Checks**: Liveness and readiness probes
6. **Resource Limits**: CPU and memory constraints
7. **Kubernetes Dashboard**: Web UI for cluster management
8. **Metrics Server**: Resource usage monitoring

## Prerequisites

- Docker installed and running
- minikube installed
- kubectl installed
- Python 3.11+ (for local testing only)

## Deployment Steps

### 1. Start minikube with required addons

```bash
minikube start
```

Enable Ingress addon:
```bash
minikube addons enable ingress
```

Enable metrics-server for HPA:
```bash
minikube addons enable metrics-server
```

Enable Kubernetes Dashboard:
```bash
minikube addons enable dashboard
```

Verify minikube is running:
```bash
kubectl get nodes
```

### 2. Configure Docker to use minikube's Docker daemon

```bash
eval $(minikube docker-env)
```

This allows Docker to build images directly into minikube's environment.

### 3. Build the Docker image

```bash
docker build -t todo-app:latest .
```

Verify the image was created:
```bash
docker images | grep todo-app
```

### 4. Deploy Kubernetes Resources

Deploy all resources in the correct order:

```bash
# 1. Create ConfigMap (application configuration)
kubectl apply -f k8s/configmap.yaml

# 2. Create Secret (sensitive data)
kubectl apply -f k8s/secret.yaml

# 3. Create Deployment
kubectl apply -f k8s/deployment.yaml

# 4. Create Service
kubectl apply -f k8s/service.yaml

# 5. Create Ingress
kubectl apply -f k8s/ingress.yaml

# 6. Create HPA (Horizontal Pod Autoscaler)
kubectl apply -f k8s/hpa.yaml
```

Or deploy all at once:
```bash
kubectl apply -f k8s/
```

### 5. Verify Deployment

Check if pods are running:
```bash
kubectl get pods
```

Check all resources:
```bash
kubectl get all
```

Check ConfigMap:
```bash
kubectl get configmap
kubectl describe configmap todo-app-config
```

Check Secret:
```bash
kubectl get secret
kubectl describe secret todo-app-secret
```

Check Service:
```bash
kubectl get svc
```

Check Ingress:
```bash
kubectl get ingress
```

Check HPA:
```bash
kubectl get hpa
kubectl describe hpa todo-app-hpa
```

View deployment status:
```bash
kubectl get deployment
kubectl describe deployment todo-app
```

### 6. Access the Application via Ingress

#### Option 1: Using minikube tunnel (Recommended)

In a separate terminal, run:
```bash
minikube tunnel
```

Add a hosts entry pointing to localhost while the tunnel is running:
```bash
echo "127.0.0.1 todo-app.local" | sudo tee -a /etc/hosts
```

Then access the application at:
```
http://todo-app.local
```

#### Option 2: Add host entry

Get minikube IP:
```bash
minikube ip
```

Add to `/etc/hosts` (Linux/macOS) or `C:\Windows\System32\drivers\etc\hosts` (Windows):
```
<minikube ip> todo-app.local
```

or combine the two steps (Linux/macOS only):
```
IP=$(minikube ip) && echo "$IP todo-app.local" | sudo tee -a /etc/hosts
``` 

Then access at:
```
http://todo-app.local
```

#### Option 3: Port forward (for testing)

```bash
kubectl port-forward service/todo-app-service 8080:80
```

Access at `http://localhost:8080`

### 7. Access Kubernetes Dashboard

Start the dashboard:
```bash
minikube dashboard
```

This will automatically open the Kubernetes Dashboard in your default browser.

Alternatively, access via port-forward:
```bash
kubectl proxy
```

Then access at:
```
http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/
```

## Kubernetes Resources

### ConfigMap
- **Name**: `todo-app-config`
- **Purpose**: Stores non-sensitive configuration data
- **Data**: APP_PORT, APP_ENV, DB_PATH, LOG_LEVEL
- **Usage**: Environment variables injected into pods

### Secret
- **Name**: `todo-app-secret`
- **Purpose**: Stores sensitive data (API keys, tokens)
- **Type**: Opaque
- **Data**: API_KEY, SECRET_TOKEN
- **Usage**: Environment variables injected into pods

### Deployment
- **Replicas**: 2 (managed by HPA: 2-5)
- **Image**: todo-app:latest
- **Port**: 5001
- **Resources**:
  - Requests: 128Mi memory, 100m CPU
  - Limits: 256Mi memory, 500m CPU
- **Health Checks**:
  - Liveness probe: `/health` endpoint
  - Readiness probe: `/health` endpoint
- **Volume**: EmptyDir volume for SQLite database storage
- **Configuration**: Uses ConfigMap and Secret for environment variables

### Service
- **Type**: ClusterIP
- **Port**: 80 (internal)
- **Target Port**: 5001 (container port)
- **Purpose**: Internal service discovery for Ingress

### Ingress
- **Name**: `todo-app-ingress`
- **Class**: nginx
- **Host**: todo-app.local
- **Purpose**: External access to the application
- **Annotations**: NGINX ingress controller configurations

### HPA (Horizontal Pod Autoscaler)
- **Name**: `todo-app-hpa`
- **Min Replicas**: 2
- **Max Replicas**: 5
- **Metrics**:
  - CPU utilization: 70%
  - Memory utilization: 80%
- **Scaling Behavior**:
  - Scale up: 100% or 2 pods per 30 seconds (max)
  - Scale down: 50% per 60 seconds (300s stabilization)

## Useful Commands

### View logs
```bash
# All pods
kubectl logs -f deployment/todo-app

# Specific pod
kubectl logs -f <pod-name>

# All pods with labels
kubectl logs -f -l app=todo-app
```

### Scale deployment manually
```bash
kubectl scale deployment todo-app --replicas=3
```

### View HPA status
```bash
kubectl get hpa
kubectl describe hpa todo-app-hpa
kubectl get hpa todo-app-hpa -w
```

### View metrics
```bash
# Node metrics
kubectl top nodes

# Pod metrics
kubectl top pods

# Pod metrics with labels
kubectl top pods -l app=todo-app
```

### Restart deployment
```bash
kubectl rollout restart deployment/todo-app
kubectl rollout status deployment/todo-app
```

### View pod details
```bash
kubectl describe pod <pod-name>
kubectl get pod <pod-name> -o yaml
```

### Exec into pod
```bash
kubectl exec -it <pod-name> -- /bin/bash
kubectl exec -it <pod-name> -- /bin/sh
```

### View environment variables in pod
```bash
kubectl exec <pod-name> -- env | grep -E 'APP_|DB_|API_|SECRET_'
```

### Test health endpoint
```bash
kubectl port-forward <pod-name> 8080:5001
curl http://localhost:8080/health
```

### Delete pods and watch recreation
```bash
kubectl delete pods -l app=todo-app
kubectl get pods -w
```

### Update ConfigMap
```bash
kubectl edit configmap todo-app-config
# After editing, restart pods to apply changes
kubectl rollout restart deployment/todo-app
```

### Update Secret
```bash
kubectl edit secret todo-app-secret
# After editing, restart pods to apply changes
kubectl rollout restart deployment/todo-app
```

### View Ingress details
```bash
kubectl describe ingress todo-app-ingress
kubectl get ingress todo-app-ingress -o yaml
```

### Check Ingress controller
```bash
kubectl get pods -n ingress-nginx
kubectl get svc -n ingress-nginx
```

## Monitoring and Observability

### Kubernetes Dashboard

Access the dashboard:
```bash
minikube dashboard
```

In the dashboard, you can:
- View all resources (Pods, Deployments, Services, Ingress, HPA)
- View pod logs
- View resource usage (CPU, Memory)
- Execute commands in pods
- View events and status

### Health Check Endpoint

The application exposes a health check endpoint:
```bash
curl http://todo-app.local/health
```

Response:
```json
{
  "status": "healthy",
  "environment": "production",
  "database": "connected"
}
```

### View Events

```bash
kubectl get events --sort-by='.lastTimestamp'
kubectl get events -w
```

### View Resource Usage

```bash
# Overall cluster usage
kubectl top nodes

# Pod resource usage
kubectl top pods

# Detailed pod metrics
kubectl describe pod <pod-name>
```

## Testing HPA

To test the Horizontal Pod Autoscaler, you can generate load:

### Option 1: Using kubectl run (simple load)
```bash
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh -c "while true; do wget -q -O- http://todo-app-service/api/todos; done"
```

### Option 2: Using Apache Bench
```bash
# Install ab (Apache Bench) if not installed
# macOS: brew install httpd
# Ubuntu: sudo apt-get install apache2-utils

# Port forward the service
kubectl port-forward service/todo-app-service 8080:80

# Generate load
ab -n 10000 -c 10 http://localhost:8080/api/todos
```

### Option 3: Using curl in a loop
```bash
while true; do curl http://todo-app.local/api/todos; sleep 0.1; done
```

Watch HPA scaling:
```bash
kubectl get hpa todo-app-hpa -w
kubectl get pods -w
```

## API Endpoints

- `GET /` - Frontend application
- `GET /api/todos` - Get all todos
- `POST /api/todos` - Create a new todo
- `PUT /api/todos/<id>` - Toggle todo completion
- `DELETE /api/todos/<id>` - Delete a todo
- `GET /health` - Health check endpoint

## Local Development

To run the application locally (without Kubernetes):

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

The database will be created as `todo.db` in the current directory. To use a different path, set the `DB_PATH` environment variable:
```bash
DB_PATH=./data/todo.db python app.py
```

3. Access at `http://localhost:5001`

## Troubleshooting

### Pods not starting
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### Ingress not working
```bash
# Check Ingress controller
kubectl get pods -n ingress-nginx
kubectl get svc -n ingress-nginx

# Check Ingress resource
kubectl describe ingress todo-app-ingress

# Check minikube tunnel
minikube tunnel
```

### HPA not scaling
```bash
# Check metrics-server
kubectl get pods -n kube-system | grep metrics-server

# Check HPA status
kubectl describe hpa todo-app-hpa

# Check pod metrics
kubectl top pods
```

### ConfigMap/Secret not applied
```bash
# Verify ConfigMap/Secret exists
kubectl get configmap todo-app-config
kubectl get secret todo-app-secret

# Restart deployment to pick up changes
kubectl rollout restart deployment/todo-app
```

### Dashboard not accessible
```bash
# Start dashboard
minikube dashboard

# Or use kubectl proxy
kubectl proxy
# Then access: http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/
```

## Cleanup

To remove all resources:
```bash
kubectl delete -f k8s/
```

To remove specific resources:
```bash
kubectl delete -f k8s/hpa.yaml
kubectl delete -f k8s/ingress.yaml
kubectl delete -f k8s/service.yaml
kubectl delete -f k8s/deployment.yaml
kubectl delete -f k8s/secret.yaml
kubectl delete -f k8s/configmap.yaml
```

To stop minikube:
```bash
minikube stop
```

To delete minikube cluster:
```bash
minikube delete
```

## Notes

- The SQLite database is stored in an EmptyDir volume, which means data will be lost when pods are deleted
- For production, consider using PersistentVolume (PV) and PersistentVolumeClaim (PVC) for data persistence
- The application uses HPA for automatic scaling based on CPU and memory usage
- ConfigMap and Secret are used to manage configuration and sensitive data separately
- Ingress provides external access with domain-based routing
- Health checks ensure pods are healthy before receiving traffic
- Resource limits prevent pods from consuming excessive cluster resources
- For production, consider using a shared database like PostgreSQL with a StatefulSet or external database service
- Secrets in this project are base64 encoded but not encrypted. For production, use sealed-secrets or external secret management

