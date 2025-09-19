#!/bin/bash

echo "🚀 Deploying E-commerce OpenLLMetry to Minikube..."

# Start Minikube if not running
if ! minikube status | grep -q "Running"; then
    echo "Starting Minikube..."
    minikube start --driver=docker --memory=4096 --cpus=2
fi

# Build Docker image in Minikube
echo "Building Docker image..."
eval $(minikube docker-env)
docker build -t ecommerce-app:latest .

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

# Get service URLs
echo "🎉 Deployment complete!"
echo ""
echo "Access your services:"
echo "📱 E-commerce App: $(minikube service ecommerce-app -n ecommerce-observability --url)"
echo "📊 Prometheus: $(minikube service prometheus -n ecommerce-observability --url)"
echo "📈 Grafana: $(minikube service grafana -n ecommerce-observability --url) (admin/admin)"
echo ""
echo "To port-forward services locally:"
echo "kubectl port-forward svc/ecommerce-app 8000:8000 -n ecommerce-observability"
echo "kubectl port-forward svc/prometheus 9090:9090 -n ecommerce-observability"
echo "kubectl port-forward svc/grafana 3000:3000 -n ecommerce-observability"