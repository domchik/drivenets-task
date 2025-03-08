#!/bin/bash
set -e

echo "Building React client..."
cd client
npm install
npm run build
echo "Build completed successfully!" 