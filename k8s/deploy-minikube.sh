#!/bin/bash
# Phase IV: Deploy TaskFlow to Minikube
# Author: Sharmeen Asif (AstolixGen Team)
# Usage: ./k8s/deploy-minikube.sh

set -e

echo "=== TaskFlow - Minikube Deployment ==="
echo "Phase IV: Local Kubernetes Deployment"
echo ""

# 1. Start Minikube if not running
echo "[1/7] Checking Minikube..."
if ! minikube status | grep -q "Running"; then
    echo "Starting Minikube..."
    minikube start --cpus 4 --memory 8192 --driver=docker
fi

# 2. Enable required addons
echo "[2/7] Enabling addons..."
minikube addons enable ingress
minikube addons enable metrics-server

# 3. Build Docker images inside Minikube
echo "[3/7] Building Docker images..."
eval $(minikube docker-env)
docker build -t taskflow-backend:latest ./backend
docker build -t taskflow-frontend:latest --build-arg NEXT_PUBLIC_API_URL=http://taskflow-backend:8000 ./frontend

# 4. Apply Kubernetes manifests
echo "[4/7] Applying K8s manifests..."
kubectl apply -f k8s/base/namespace.yaml
kubectl apply -f k8s/base/secrets.yaml
kubectl apply -f k8s/base/postgres-deployment.yaml

echo "Waiting for PostgreSQL..."
kubectl wait --for=condition=ready pod -l app=postgres -n taskflow --timeout=120s

# 5. Deploy backend & frontend
echo "[5/7] Deploying application..."
kubectl apply -f k8s/base/backend-deployment.yaml
kubectl apply -f k8s/base/frontend-deployment.yaml
kubectl apply -f k8s/base/ingress.yaml

# 6. Wait for pods
echo "[6/7] Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=taskflow-backend -n taskflow --timeout=120s
kubectl wait --for=condition=ready pod -l app=taskflow-frontend -n taskflow --timeout=120s

# 7. Show status
echo "[7/7] Deployment complete!"
echo ""
echo "=== Pod Status ==="
kubectl get pods -n taskflow
echo ""
echo "=== Services ==="
kubectl get svc -n taskflow
echo ""

# Get access URL
FRONTEND_URL=$(minikube service taskflow-frontend -n taskflow --url 2>/dev/null || echo "pending")
echo "Frontend URL: $FRONTEND_URL"
echo ""
echo "Or add to /etc/hosts: $(minikube ip) taskflow.local"
echo "Then visit: http://taskflow.local"
