# Use the official Lambda base image for Python 3.11
FROM public.ecr.aws/lambda/python:3.11

# Install system dependencies
RUN yum install -y \
    libXext \
    libXrender \
    libSM \
    libX11 \
    ghostscript \
    tesseract \
    tesseract-langpack-eng \
    && yum clean all

# Set the working directory to /var/task
WORKDIR /var/task

# Copy the local code and requirements to the container
COPY lambda_function.py .
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download the OCRmyPDF dependencies to /var/task
RUN curl -sSL https://bootstrap.pypa.io/get-pip.py | python3 - \
    && pip install --no-cache-dir ocrmypdf
    
# Bundle the layers
#RUN cd /var/task && \
 #   zip -r /opt/layer.zip *

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.lambda_handler" ]
