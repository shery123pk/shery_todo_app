#!/bin/bash
# Kubernetes Deployment Script for Todo Application
# Phase IV: Local Minikube Deployment
# Author: Sharmeen Asif

set -e

echo "========================================="
echo "Todo App - Kubernetes Deployment"
echo "========================================="

# Check if minikube is running
if ! minikube status | grep -q "Running"; then
    echo "Starting Minikube..."
    minikube start --driver=docker --cpus=4 --memory=4096
fi

# Enable Minikube addons
echo "Enabling Minikube addons..."
minikube addons enable ingress
minikube addons enable metrics-server

# Use Minikube's Docker daemon
echo "Switching to Minikube Docker daemon..."
eval $(minikube docker-env)

# Build Docker images
echo "Building Docker images..."
echo " - Building backend image..."
docker build -t todo-backend:latest ../backend/

echo " - Building frontend image..."
docker build -t todo-frontend:latest ../frontend/

echo " - Building chatbot image..."
docker build -t todo-chatbot:latest ../chatbot/

# Apply Kubernetes manifests
echo "Applying Kubernetes manifests..."
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secrets.yaml
kubectl apply -f postgres.yaml
kubectl apply -f backend.yaml
kubectl apply -f frontend.yaml
kubectl apply -f chatbot.yaml

# Wait for deployments
echo "Waiting for deployments to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/postgres -n todo-app
kubectl wait --for=condition=available --timeout=300s deployment/backend -n todo-app
kubectl wait --for=condition=available --timeout=300s deployment/frontend -n todo-app

# Get service URLs
echo ""
echo "========================================="
echo "Deployment Complete!"
echo "========================================="
echo ""
echo "Access the application:"
echo " - Frontend: $(minikube service frontend-service -n todo-app --url)"
echo " - Backend API: $(minikube service backend-service -n todo-app --url)"
echo ""
echo "View pods:"
echo "  kubectl get pods -n todo-app"
echo ""
echo "View logs:"
echo "  kubectl logs -f deployment/backend -n todo-app"
echo "  kubectl logs -f deployment/frontend -n todo-app"
echo ""
echo "Access chatbot:"
echo "  kubectl exec -it deployment/chatbot -n todo-app -- python -m app.main"
echo ""
echo "Dashboard:"
echo "  minikube dashboard"
echo ""
