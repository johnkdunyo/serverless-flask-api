#!/bin/bash

# DynamoDB table name
TABLE_NAME="flask-app-db"

# AWS credentials and region configuration for local environment
AWS_REGION="local"

# Sample blog data
BLOG_DATA='[
    {
        "blog_id": "1",
        "title": "Introduction to DynamoDB (Local)",
        "content": "DynamoDB is a fully managed NoSQL database service provided by AWS.",
        "author": "John Doe",
        "created_at": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'"
    },
    {
        "blog_id": "2",
        "title": "Deep Dive into DynamoDB Partitioning (Local)",
        "content": "Understanding how DynamoDB partitions data is crucial for optimal performance.",
        "author": "Jane Smith",
        "created_at": "'$(date -u -d '-7 days' +"%Y-%m-%dT%H:%M:%SZ")'"
    }
    # Add more blog entries as needed
]'

# Seed DynamoDB table
echo "Seeding DynamoDB table..."
aws dynamodb put-item --table-name "$TABLE_NAME" --item "$BLOG_DATA" --region "$AWS_REGION" --profile default
echo "Seeding completed."

# Note: Adjust the "aws" command based on your AWS CLI configuration (profile, region, etc.)
