#!/bin/bash
# Phase V: Deploy TaskFlow to DigitalOcean DOKS
# Author: Sharmeen Asif (AstolixGen Team)
# Prerequisites: doctl, kubectl, helm installed and configured
# Usage: ./k8s/deploy-cloud.sh

set -e

CLUSTER_NAME="taskflow-cluster"
REGION="nyc1"
NODE_SIZE="s-2vcpu-4gb"
NODE_COUNT=2

echo "=== TaskFlow - Cloud Deployment (DigitalOcean DOKS) ==="
echo "Phase V: Advanced Cloud Deployment"
echo ""

# 1. Create DOKS cluster (if not exists)
echo "[1/8] Creating DOKS cluster..."
if ! doctl kubernetes cluster get $CLUSTER_NAME &>/dev/null; then
    doctl kubernetes cluster create $CLUSTER_NAME \
        --region $REGION \
        --size $NODE_SIZE \
        --count $NODE_COUNT \
        --tag taskflow
    echo "Cluster created. Waiting for ready state..."
    sleep 30
fi

# 2. Configure kubectl
echo "[2/8] Configuring kubectl..."
doctl kubernetes cluster kubeconfig save $CLUSTER_NAME

# 3. Install Dapr
echo "[3/8] Installing Dapr runtime..."
if ! kubectl get namespace dapr-system &>/dev/null; then
    helm repo add dapr https://dapr.github.io/helm-charts/
    helm repo update
    helm install dapr dapr/dapr --namespace dapr-system --create-namespace --wait
fi

# 4. Install Kafka via Helm
echo "[4/8] Installing Kafka..."
if ! kubectl get namespace kafka &>/dev/null; then
    helm repo add bitnami https://charts.bitnami.com/bitnami
    helm install kafka bitnami/kafka \
        --namespace taskflow --create-namespace \
        --set kraft.enabled=true \
        --set listeners.client.protocol=PLAINTEXT \
        --wait
fi

# 5. Apply base manifests
echo "[5/8] Deploying TaskFlow..."
kubectl apply -f k8s/base/namespace.yaml
kubectl apply -f k8s/base/secrets.yaml
kubectl apply -f k8s/base/postgres-deployment.yaml

echo "Waiting for PostgreSQL..."
kubectl wait --for=condition=ready pod -l app=postgres -n taskflow --timeout=180s

# 6. Deploy with Dapr sidecars
echo "[6/8] Deploying with Dapr..."
kubectl apply -f k8s/dapr/dapr-components.yaml
kubectl apply -f k8s/dapr/dapr-backend-sidecar.yaml
kubectl apply -f k8s/base/frontend-deployment.yaml
kubectl apply -f k8s/base/ingress.yaml

# 7. Wait for readiness
echo "[7/8] Waiting for all pods..."
kubectl wait --for=condition=ready pod -l app=taskflow-backend -n taskflow --timeout=180s
kubectl wait --for=condition=ready pod -l app=taskflow-frontend -n taskflow --timeout=180s

# 8. Show status
echo "[8/8] Cloud deployment complete!"
echo ""
echo "=== Cluster Info ==="
kubectl cluster-info
echo ""
echo "=== Pod Status ==="
kubectl get pods -n taskflow
echo ""
echo "=== Services ==="
kubectl get svc -n taskflow
echo ""
echo "=== External IP ==="
kubectl get ingress -n taskflow
echo ""
echo "To monitor with kubectl-ai: kubectl-ai 'show taskflow pod health'"
