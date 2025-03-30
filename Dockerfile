# Use an official Python runtime as a parent image
FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl

RUN bash -c 'if ! [[ "9 10 11 12" == *"$(grep VERSION_ID /etc/os-release | cut -d "\"" -f 2 | cut -d "." -f 1)"* ]]; then \
        echo "Debian $(grep VERSION_ID /etc/os-release | cut -d "\"" -f 2 | cut -d "." -f 1) is not currently supported."; \
        exit 1; \
    fi && \
    # Download and install Microsoft repo package
    curl -sSL -O https://packages.microsoft.com/config/debian/$(grep VERSION_ID /etc/os-release | cut -d "\"" -f 2 | cut -d '.' -f 1)/packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    rm packages-microsoft-prod.deb && \
    # Update apt-get and install msodbcsql18
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18'

# Set the working directory in the container
WORKDIR /app

# Create a non-root user and switch to it
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Copy the current directory contents into the container at /app
COPY --chown=appuser:appgroup . /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Change to non-root user
USER appuser

# Run main.py when the container launches
ENTRYPOINT ["python", "__main__.py"]
