# E-commerce OpenLLMetry Observability

A production-ready e-commerce application with comprehensive observability using OpenLLMetry, Prometheus, and Grafana.

## 🌟 New Features

- ✅ **Complete Web Interface** - Beautiful HTML frontend with interactive features
- ✅ **Docker Containerization** - Production-ready Docker image
- ✅ **DockerHub Integration** - Available at `dockerworld87/ecommerce-openllmetry`
- ✅ **Environment Variable Support** - Configurable OpenAI API key
- ✅ **Health Checks** - Built-in container health monitoring
- ✅ **Security Hardening** - Non-root user, optimized layers

## 🏗️ Architecture

- **E-commerce Services**: Product catalog, cart, recommendations, chatbot
- **OpenLLMetry**: Automatic LLM observability instrumentation
- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and alerting
- **OpenTelemetry**: Standardized telemetry collection

## 🚀 Quick Start

### Option 1: Run from DockerHub (Recommended)
```bash
# Run with simulated AI (no API key needed)
docker run -d -p 8000:8000 dockerworld87/ecommerce-openllmetry:latest

# Run with real OpenAI API
docker run -d -p 8000:8000 -e OPENAI_API_KEY="your-key-here" dockerworld87/ecommerce-openllmetry:latest

# Access the application
open http://localhost:8000
```

### Option 2: Build and Run Locally
```bash
# Clone repository
git clone https://github.com/Soumya14041987/ecommerce-openllmetry-observability.git
cd ecommerce-openllmetry-observability

# Build and run
./run-local.sh

# Or manually
docker build -t ecommerce-openllmetry:latest .
docker run -d -p 8000:8000 ecommerce-openllmetry:latest
```

### Option 3: Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables (optional)
export OPENAI_API_KEY="your-openai-key"

# Run application
python3 app/main.py
```

## 🌐 Web Interface Features

The application now includes a complete web interface with:

- **📦 Product Catalog** - Browse available products
- **🤖 AI Recommendations** - Get personalized product suggestions
- **🔍 Semantic Search** - AI-powered product search
- **💬 Customer Support Chat** - Interactive AI chatbot
- **📊 Live Metrics Dashboard** - Real-time application metrics
- **📱 Responsive Design** - Works on desktop and mobile

## 🐳 Docker Deployment

### Available Images
- `dockerworld87/ecommerce-openllmetry:latest` - Latest version
- `dockerworld87/ecommerce-openllmetry:v1.0.0` - Stable release

### Push to DockerHub
```bash
# Login and push (for maintainers)
./scripts/deploy-dockerhub.sh
```

### Docker Compose
```bash
# Full stack with monitoring
docker-compose up -d

# Access services
# Application: http://localhost:8000
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000 (admin/admin)
```

## ☸️ Kubernetes Deployment

### Minikube
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

### EKS
```bash
# Create EKS cluster
eksctl create cluster --name ecommerce-obs --region us-west-2

# Deploy application
kubectl apply -f k8s/

# Get LoadBalancer URLs
kubectl get svc
```

### EC2
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

### LLM Metrics Tracked
- **Token Usage**: Input/output tokens, costs
- **Performance**: Response times, throughput
- **Quality**: Success rates, error types
- **Business**: User interactions, conversions

### Dashboards Available
- **OpenLLMetry Dashboard**: LLM-specific metrics and costs
- **Application Performance**: Response times, throughput, errors
- **Business Intelligence**: User behavior and engagement
- **Infrastructure Health**: System resources and capacity

## 🛠️ API Endpoints

- `GET /` - Web interface
- `GET /health` - Health check
- `GET /products` - Product catalog
- `POST /recommendations` - AI recommendations
- `POST /chatbot` - Customer support chat
- `POST /search` - Semantic search
- `GET /metrics` - Application metrics
- `GET /docs` - API documentation

## 🧪 Testing

### Manual Testing
```bash
# Health check
curl http://localhost:8000/health

# Get products
curl http://localhost:8000/products

# AI recommendation
curl -X POST http://localhost:8000/recommendations \
  -H "Content-Type: application/json" \
  -d '{"query": "laptop for programming", "budget": 1500}'

# Chatbot
curl -X POST http://localhost:8000/chatbot \
  -H "Content-Type: application/json" \
  -d '{"message": "What is your return policy?"}'
```

### Automated Testing
```bash
# Run test suite
python scripts/test-application.py

# Load testing
python scripts/test-application.py --load-test --requests 50
```

## 🔧 Configuration

### Environment Variables
```bash
# Required for real AI features
OPENAI_API_KEY=your-openai-api-key-here

# Optional OpenTelemetry configuration
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318
OTEL_SERVICE_NAME=ecommerce-service
OTEL_SERVICE_VERSION=1.0.0

# Application settings
APP_NAME=ecommerce-app
DEBUG=false
```

### Docker Environment File
```bash
# Copy example environment file
cp .env.example .env

# Edit with your settings
nano .env
```

## 📈 Monitoring Stack Access

- **Application**: http://localhost:8000
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)
- **API Documentation**: http://localhost:8000/docs

## 🔒 Security Features

- **Non-root container user** for security
- **Health checks** for container orchestration
- **Environment variable** configuration
- **Input validation** and error handling
- **CORS protection** for web interface

## 📚 Documentation

- [OpenLLMetry Documentation](https://www.traceloop.com/docs/openllmetry/introduction)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the Apache 2.0 License - see the LICENSE file for details.