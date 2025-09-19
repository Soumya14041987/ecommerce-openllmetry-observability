#!/bin/bash

CLUSTER_NAME="ecommerce-obs"
REGION="us-west-2"

echo "🚀 Deploying E-commerce OpenLLMetry to EKS..."

# Check if eksctl is installed
if ! command -v eksctl &> /dev/null; then
    echo "❌ eksctl is not installed. Please install it first."
    echo "Visit: https://eksctl.io/introduction/#installation"
    exit 1
fi

# Check if cluster exists
if ! eksctl get cluster --name $CLUSTER_NAME --region $REGION &> /dev/null; then
    echo "Creating EKS cluster..."
    eksctl create cluster \
        --name $CLUSTER_NAME \
        --region $REGION \
        --node-type t3.medium \
        --nodes 3 \
        --nodes-min 1 \
        --nodes-max 4 \
        --managed
else
    echo "EKS cluster $CLUSTER_NAME already exists"
fi

# Update kubeconfig
aws eks update-kubeconfig --region $REGION --name $CLUSTER_NAME

# Build and push Docker image to ECR
echo "Setting up ECR repository..."
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REPO="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/ecommerce-app"

# Create ECR repository if it doesn't exist
aws ecr describe-repositories --repository-names ecommerce-app --region $REGION || \
aws ecr create-repository --repository-name ecommerce-app --region $REGION

# Login to ECR
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ECR_REPO

# Build and push image
docker build -t ecommerce-app:latest .
docker tag ecommerce-app:latest $ECR_REPO:latest
docker push $ECR_REPO:latest

# Update Kubernetes manifests with ECR image
sed -i.bak "s|image: ecommerce-app:latest|image: $ECR_REPO:latest|g" k8s/ecommerce-app.yaml

# Apply Kubernetes manifests
echo "Applying Kubernetes manifests..."
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/otel-collector.yaml
kubectl apply -f k8s/prometheus.yaml
kubectl apply -f k8s/grafana.yaml

# Update OpenAI API key secret
echo "Please update the OpenAI API key in k8s/ecommerce-app.yaml before deploying the app"
read -p "Press enter to continue after updating the API key..."

kubectl apply -f k8s/ecommerce-app.yaml

# Wait for deployments
echo "Waiting for deployments to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/otel-collector -n ecommerce-observability
kubectl wait --for=condition=available --timeout=300s deployment/prometheus -n ecommerce-observability
kubectl wait --for=condition=available --timeout=300s deployment/grafana -n ecommerce-observability
kubectl wait --for=condition=available --timeout=300s deployment/ecommerce-app -n ecommerce-observability

# Get LoadBalancer URLs
echo "🎉 Deployment complete!"
echo ""
echo "Getting service URLs (this may take a few minutes)..."
echo "📱 E-commerce App: $(kubectl get svc ecommerce-app -n ecommerce-observability -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'):8000"
echo "📊 Prometheus: $(kubectl get svc prometheus -n ecommerce-observability -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'):9090"
echo "📈 Grafana: $(kubectl get svc grafana -n ecommerce-observability -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'):3000 (admin/admin)"

# Restore original manifest
mv k8s/ecommerce-app.yaml.bak k8s/ecommerce-app.yaml