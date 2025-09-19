# E-commerce OpenLLMetry Observability

A production-ready e-commerce application with comprehensive observability using OpenLLMetry, Prometheus, and Grafana.

## 🏗️ Architecture

- **E-commerce Services**: Product catalog, cart, recommendations, chatbot
- **OpenLLMetry**: Automatic LLM observability instrumentation
- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and alerting
- **OpenTelemetry**: Standardized telemetry collection

## 🚀 Quick Start

### Local Development
```bash
# Clone repository
git clone https://github.com/Soumya14041987/ecommerce-openllmetry-observability.git
cd ecommerce-openllmetry-observability

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="your-openai-key"

# Run application
python app/main.py
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d

# Access services
# Application: http://localhost:8000
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000 (admin/admin)
```

### Kubernetes Deployment

#### Minikube
```bash
# Start Minikube
minikube start

# Deploy application
kubectl apply -f k8s/

# Port forward services
kubectl port-forward svc/ecommerce-app 8000:8000
kubectl port-forward svc/prometheus 9090:9090
kubectl port-forward svc/grafana 3000:3000
```

#### EKS
```bash
# Create EKS cluster
eksctl create cluster --name ecommerce-obs --region us-west-2

# Deploy application
kubectl apply -f k8s/

# Get LoadBalancer URLs
kubectl get svc
```

#### EC2
```bash
# Install Docker and Docker Compose on EC2
sudo yum update -y
sudo yum install -y docker
sudo systemctl start docker
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone and run
git clone https://github.com/Soumya14041987/ecommerce-openllmetry-observability.git
cd ecommerce-openllmetry-observability
sudo docker-compose up -d
```

## 📊 Observability Features

- **LLM Metrics**: Token usage, costs, latency, error rates
- **Business Metrics**: Sales, user interactions, recommendations
- **Infrastructure Metrics**: CPU, memory, network, disk
- **Distributed Tracing**: End-to-end request tracking
- **Custom Dashboards**: Pre-built Grafana dashboards
- **Alerting**: Prometheus alerts for critical metrics

## 🛠️ Services

- **Product Service**: AI-powered product recommendations
- **Cart Service**: Shopping cart with intelligent suggestions
- **Chatbot Service**: Customer support AI assistant
- **Search Service**: Semantic product search
- **Analytics Service**: Business intelligence and insights

## 📈 Monitoring

Access the monitoring stack:
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **Application**: http://localhost:8000

## 🔧 Configuration

Environment variables:
- `OPENAI_API_KEY`: OpenAI API key for LLM services
- `OTEL_EXPORTER_OTLP_ENDPOINT`: OpenTelemetry collector endpoint
- `PROMETHEUS_URL`: Prometheus server URL

## 📚 Documentation

- [OpenLLMetry Documentation](https://www.traceloop.com/docs/openllmetry/introduction)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)