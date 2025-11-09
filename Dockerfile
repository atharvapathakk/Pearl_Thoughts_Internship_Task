# Use a lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependencies file first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app files
COPY . .

# After COPY . .
RUN mkdir -p /app/instance


# Expose the port Cloud Run expects
EXPOSE 8080

# Run the app
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
#CMD ["gunicorn", "-b", "0.0.0.0:8080", "run:app"]



#to run the docekr file run this command 
#docker run -v $(pwd)/instance:/app/instance -p 5051:8080 stock-analyzer
#chaeg the port to 5051 to 8080 if its not wotking 





# now tomorrows target to return the docekr file to normal and then reldeploy it in gcp tomrrow evrything ctrl z and comment the uncommetn the code on 21 aug 