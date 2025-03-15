# Use a lightweight Python base image
FROM python:3.12-slim

# Set environment variables for better behavior
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install uv
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy only dependency files first to leverage caching
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync --frozen

# Copy the rest of the application
COPY . .

# So that appuser can create team_history.json and team_state.json
RUN useradd -m appuser && \
    chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Expose the application port
EXPOSE 8000

# Start the FastAPI app using uvicorn
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
