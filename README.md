# Kubernetes Hands-On Project 

A lightweight full-stack ToDo application deployed on Kubernetes (minikube) to demonstrate hands-on Kubernetes experience. This project showcases containerization with Docker and orchestration with Kubernetes.

## Project Overview

- **Backend**: Flask REST API (Python)
- **Frontend**: Vanilla JavaScript, HTML, CSS
- **Database**: SQLite
- **Containerization**: Docker
- **Orchestration**: Kubernetes (minikube)
- **Deployment**: Kubernetes Deployment and Service

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
│   ├── deployment.yaml
│   └── service.yaml
└── README.md
```

## Technologies Used

- **Flask**: Python web framework
- **SQLite**: Lightweight database
- **Docker**: Containerization
- **Kubernetes**: Container orchestration
- **minikube**: Local Kubernetes cluster

## Prerequisites

- Docker installed and running
- minikube installed
- kubectl installed
- Python 3.11+ (for local testing only)

## Deployment Steps

### 1. Start minikube

```bash
minikube start
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

### 4. Deploy to Kubernetes

Deploy the application using the Kubernetes manifests:

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### 5. Verify Deployment

Check if pods are running:
```bash
kubectl get pods
```

Check the service:
```bash
kubectl get svc
```

View deployment status:
```bash
kubectl get deployment
```

### 6. Access the Application

Get the minikube IP and NodePort:
```bash
minikube ip
```

The service is exposed on NodePort 30080. Access the application at:
```
http://<minikube-ip>:30080
```

Alternatively, use minikube service command:
```bash
minikube service todo-app-service
```

This will automatically open the application in your default browser.

## Kubernetes Resources

### Deployment
- **Replicas**: 2 (for high availability)
- **Image**: todo-app:latest
- **Port**: 5001
- **Volume**: EmptyDir volume for SQLite database storage

### Service
- **Type**: NodePort
- **Port**: 80 (internal)
- **Target Port**: 5001 (container port)
- **NodePort**: 30080 (external access)

## Useful Commands

### View logs
```bash
kubectl logs -f deployment/todo-app
```

### Scale deployment
```bash
kubectl scale deployment todo-app --replicas=3
```

### Restart deployment
```bash
kubectl rollout restart deployment/todo-app
```

### View pod details
```bash
kubectl describe pod <pod-name>
```

### Exec into pod
```bash
kubectl exec -it <pod-name> -- /bin/bash
```

### Delete pods and redeploy pods
```bash
kubectl delete pods -l app=todo-app
kubectl get pods -w
```

### Delete deployment
```bash
kubectl delete -f k8s/deployment.yaml
kubectl delete -f k8s/service.yaml
```

## Cleanup

To remove all resources:
```bash
kubectl delete -f k8s/
```

To stop minikube:
```bash
minikube stop
```

To delete minikube cluster:
```bash
minikube delete
```

## API Endpoints

- `GET /api/todos` - Get all todos
- `POST /api/todos` - Create a new todo
- `PUT /api/todos/<id>` - Toggle todo completion
- `DELETE /api/todos/<id>` - Delete a todo

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

## Notes

- The SQLite database is stored in an EmptyDir volume, which means data will be lost when pods are deleted
- For production, consider using PersistentVolume (PV) and PersistentVolumeClaim (PVC) for data persistence
- The application uses 2 replicas for demonstration, but they share the same volume (data consistency not guaranteed in this setup)
- For production, consider using a shared database like PostgreSQL with a StatefulSet or external database service
