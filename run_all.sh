#!/bin/bash

REACT_DIR="./frontend/lyrebird"  # The React project directory
DJANGO_DIR="./backend/lyrebird"  # The Django project directory

# # Step 1: Check if directories exist
if [ ! -d "$REACT_DIR" ]; then
    echo "React.js project directory not found at $REACT_DIR"
    exit 1
fi

if [ ! -d "$DJANGO_DIR" ]; then
    echo "Django project directory not found at $DJANGO_DIR"
    exit 1
fi

# Step 2: Install Node.js dependencies (React.js)
echo "Installing Node.js dependencies for React.js project..."
cd "$REACT_DIR"  # Navigate to the React project directory
if [ ! -d "node_modules" ]; then
    npm install  # Install dependencies only if node_modules directory doesn't exist
else
    echo "Node.js dependencies already installed"
fi

# Step 3: Start React.js project
echo "Starting React.js project..."
npm run dev &  # Start React development server in the background

Wait for React server to start
sleep 5

# Step 4: Install Python dependencies (Django)
echo "Installing Python dependencies for Django project..."
cd "$DJANGO_DIR"  # Navigate to the Django project directory
python3 -m venv venv

source venv/bin/activate  # Activate virtual environment
pip install -r requirements.txt  # Install dependencies from requirements.txt
python manage.py migrate  # Apply any migrations
python manage.py runserver 0.0.0.0:8000 &  # Start Django development server in the background

# Step 5: Start RabbitMQ Docker container
echo "Starting RabbitMQ in Docker..."
docker run -d --hostname rabbit -p 5672:5672 -p 15672:15672 -e RABBITMQ_DEFAULT_USER=cool -e RABBITMQ_DEFAULT_PASS=test3142 -e RABBITMQ_DEFAULT_VHOST=lyrebird -v $HOME/docker_volumes/rabbitmq:/var/lib/rabbitmq --name rabbitmq rabbitmq:3-management

# # Wait for RabbitMQ to start
# sleep 10


# Wait for Django server to start
sleep 5

# Step 7: Run Django Management Commands (to listen to RabbitMQ Queues)
echo "Running Django management commands..."

# Command 1 (replace with your actual management command)
python manage.py audio_storage_processor &

# Command 2 (replace with your actual management command)
python manage.py speech_text_converter &

# Wait for all processes to finish
wait
