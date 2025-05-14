#!/bin/bash

# Backend
cd backend
serverless deploy

# Frontend
cd ../frontend
npm run build
amplify publish