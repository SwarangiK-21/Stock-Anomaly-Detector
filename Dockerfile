# 1. Start with a lightweight Python installation (The "Base Layer")
FROM python:3.9-slim

# 2. Set the working directory inside the container (The "Kitchen")
WORKDIR /app

# 3. Copy the grocery list (requirements) into the container
COPY requirements.txt .

# 4. Install the libraries inside the container
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy all your code (main.py, etc.) into the container
COPY . .

# 6. The command to run your app when the container starts
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]