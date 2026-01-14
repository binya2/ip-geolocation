# IP Geolocation Microservices with Kubernetes 🌍

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95-009688?style=flat&logo=fastapi)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Minikube-326ce5?style=flat&logo=kubernetes)
![Redis](https://img.shields.io/badge/Redis-Cache-red?style=flat&logo=redis)

A robust microservices architecture project that fetches IP geolocation data, caches it in Redis, and runs on a Kubernetes cluster.

## 🏗 Architecture

The system consists of two main microservices and a database:

1.  **Service A (Gateway/Logic):**
    * Exposes REST endpoints to clients.
    * Fetches geolocation data from an external provider (IP2Location).
    * Orchestrates data flow to Service B.
2.  **Service B (Data Access Layer):**
    * Manages communication with Redis.
    * Stores and retrieves cached geolocation data.
3.  **Redis:**
    * Stateful backend for caching.

## 📂 Project Structure

```text
.
├── k8s/                  # Kubernetes manifests (Deployments, Services, StatefulSet)
├── service-a/            # Gateway Service (Python/FastAPI)
├── service-b/            # Storage Service (Python/FastAPI)
├── shared/               # Shared Pydantic schemas
└── README.md             # Project documentation
```

## 🚀 Prerequisites

* [Docker](https://www.docker.com/) installed.
* [Minikube](https://minikube.sigs.k8s.io/docs/start/) installed and running.
* [kubectl](https://kubernetes.io/docs/tasks/tools/) configured.

---

## 🛠️ Installation & Setup

### 1. Build Docker Images
**Important:** You must run these commands from the root directory of the project to allow access to the `shared` folder.

Replace `your-username` with your Docker Hub username.

```bash
# Build Service A
docker build -f service-a/app/Dockerfile -t your-username/service-a:01 .

# Build Service B
docker build -f service-b/app/Dockerfile -t your-username/service-b:01 .
```

### 2. Push Images
Required for Minikube to pull the images (unless using `minikube docker-env`).

```bash
docker push your-username/service-a:01
docker push your-username/service-b:01
```

### 3. Kubernetes Configuration
Before deploying, make sure to update the `image` field in `k8s/api-deployment-a.yaml` and `k8s/api-deployment-b.yaml` with your image names.

**Create a Secret for sensitive data:**
Instead of hardcoding the API Key, create a secret in the cluster:
```bash
kubectl create secret generic app-secrets --from-literal=API_KEY=YOUR_REAL_IP2LOCATION_KEY
```

### 4. Deploy to Minikube
Apply all manifests in the `k8s` folder:

```bash
kubectl apply -f k8s/
```

Verify that pods are running:
```bash
kubectl get pods
```

---

## 🔌 Usage

Since the services use `ClusterIP`, they are not exposed externally by default. Use port-forwarding to access them.

### Access Service A (Gateway)
```bash
kubectl port-forward svc/api-service-a 8000:8000
```

Now you can send requests to `localhost:8000`:

* **Get IP Details:**
    ```bash
    curl http://localhost:8000/get-ip/8.8.8.8
    ```

* **Get All Cached IPs:**
    ```bash
    curl http://localhost:8000/get-all-ips
    ```

### Access Service B (Directly - Debugging)
```bash
kubectl port-forward svc/redis-api 8001:8000
```
Check health: `curl http://localhost:8001/health`

---

## 🧹 Cleanup

To remove all resources created by this project:

```bash
kubectl delete -f k8s/
kubectl delete secret app-secrets
```

To stop Minikube:
```bash
minikube stop
```