#!/bin/bash

# Navigate to backend directory
cd backend

# Create a clean directory for the deployment package
rm -rf lambda_package
mkdir lambda_package

# Install dependencies into the package directory
pip install -r requirements.txt --target lambda_package

# Copy backend code to the package directory
cp *.py lambda_package/

# Create the ZIP file
cd lambda_package
zip -r ../lambda_function.zip .

# Clean up
cd ..
rm -rf lambda_package

echo "Lambda deployment package created: lambda_function.zip"