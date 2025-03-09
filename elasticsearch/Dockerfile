FROM python:3.11

WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy Django project
COPY . /app/

# Expose port 8030
EXPOSE 8030

# # Run uvicorn server
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8030"]

#run development server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8030", "--reload"]