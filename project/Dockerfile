# Use a Python base image in version 3.8
FROM python:3.8

# Expose the application port 3111
EXPOSE 3111

# copy all the files from the current directory to the container working directory
COPY ./techtrends ./techtrends

# set the working directory to ./techtreads
WORKDIR ./techtrends

# Install packages defined in the requirements.txt file
RUN pip install -r requirements.txt

# Ensure that the database is initialized with the pre-defined posts in the init_db.py file
RUN python init_db.py

# Run the application
CMD ["python", "app.py"]