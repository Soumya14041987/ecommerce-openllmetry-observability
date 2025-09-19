#!/bin/bash

echo "🚀 Deploying E-commerce OpenLLMetry to EC2..."

# Update system
sudo yum update -y

# Install Docker
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    sudo yum install -y docker
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -a -G docker ec2-user
fi

# Install Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Install Git if not present
if ! command -v git &> /dev/null; then
    echo "Installing Git..."
    sudo yum install -y git
fi

# Clone repository if not exists
if [ ! -d "ecommerce-openllmetry-observability" ]; then
    echo "Cloning repository..."
    git clone https://github.com/Soumya14041987/ecommerce-openllmetry-observability.git
fi

cd ecommerce-openllmetry-observability

# Set up environment variables
echo "Setting up environment variables..."
if [ ! -f .env ]; then
    cat > .env << EOF
OPENAI_API_KEY=your-openai-api-key-here
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318
EOF
    echo "⚠️  Please update the .env file with your OpenAI API key"
    echo "Edit the file: nano .env"
    read -p "Press enter to continue after updating the API key..."
fi

# Build and start services
echo "Building and starting services..."
sudo docker-compose build
sudo docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 30

# Check service status
echo "Checking service status..."
sudo docker-compose ps

# Get EC2 public IP
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)

echo "🎉 Deployment complete!"
echo ""
echo "Access your services:"
echo "📱 E-commerce App: http://$PUBLIC_IP:8000"
echo "📊 Prometheus: http://$PUBLIC_IP:9090"
echo "📈 Grafana: http://$PUBLIC_IP:3000 (admin/admin)"
echo ""
echo "Make sure your EC2 security group allows inbound traffic on ports 3000, 8000, and 9090"
echo ""
echo "To view logs:"
echo "sudo docker-compose logs -f"
echo ""
echo "To stop services:"
echo "sudo docker-compose down"