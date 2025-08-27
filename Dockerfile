# ---- Builder Stage ----
# This stage installs build tools and compiles Python dependencies into wheels.
# To build for an NVIDIA GPU on Linux, we start from the official CUDA development image,
# which contains the necessary compilers and libraries.
FROM nvidia/cuda:12.3.2-devel-ubuntu22.04 AS builder

# Install Python and build essentials into the CUDA image.
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 python3-pip build-essential cmake git ninja-build \
    && rm -rf /var/lib/apt/lists/*

# Create a directory for the wheels.
WORKDIR /wheels

# Copy only the requirements file to leverage layer caching.
COPY requirements.txt .

# Set build arguments for llama-cpp-python to enable NVIDIA GPU support.
ENV CMAKE_ARGS="-DGGML_CUDA=on"

# Build the wheels from requirements.txt in multiple steps for better caching.
# Step 1: Build PyTorch first, using the CUDA-specific index.
RUN pip wheel \
    --extra-index-url https://download.pytorch.org/whl/cu121 \
    --wheel-dir=/wheels \
    torch

# Step 2: Build llama-cpp-python with CUDA support.
RUN pip wheel \
    --extra-index-url https://download.pytorch.org/whl/cu121 \
    --wheel-dir=/wheels \
    llama-cpp-python

# Step 3: Build the other heavy ML libraries.
RUN grep -E "transformers|sentencepiece|accelerate|peft|bitsandbytes|datasets|trl" requirements.txt > requirements-ml.txt && \
    pip wheel \
    --extra-index-url https://download.pytorch.org/whl/cu121 \
    --wheel-dir=/wheels \
    -r requirements-ml.txt

# Step 4: Build the remaining lightweight application dependencies.
RUN grep -v -E "torch|llama-cpp-python|transformers|sentencepiece|accelerate|peft|bitsandbytes|datasets|trl" requirements.txt > requirements-app.txt && \
    pip wheel \
    --extra-index-url https://download.pytorch.org/whl/cu121 \
    --wheel-dir=/wheels \
    -r requirements-app.txt

# ---- Final Stage (for NVIDIA CUDA) ----
# Use the lean NVIDIA CUDA runtime image for the final stage.
FROM nvidia/cuda:12.3.2-runtime-ubuntu22.04

# Install gosu for privilege dropping and Python for the application.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gosu python3.11 python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user for security.
RUN useradd --create-home --shell /bin/bash appuser

# Set working directory.
WORKDIR /app

# Copy the built wheels from the builder stage.
COPY --from=builder /wheels /wheels

# Install the wheels.
RUN pip install --no-cache-dir /wheels/*.whl && rm -rf /wheels

# Copy the application code and assets.
COPY ./app .
COPY ./static ./static
COPY ./templates ./templates

# Copy the entrypoint script.
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# Create directories for mounted volumes and set permissions.
RUN mkdir -p /app/data && chown -R appuser:appuser /app/data

# Change ownership of the app directory.
RUN chown -R appuser:appuser /app

# Set the PYTHONPATH.
ENV PYTHONPATH=/app

# Expose the port.
EXPOSE 8000

ENTRYPOINT ["entrypoint.sh"]
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]