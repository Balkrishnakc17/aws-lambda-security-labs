# Lab 02 - S3 Security Auditor

> 🚧 Work in Progress

## Objective

The objective of this lab is to build an automated S3 security auditor using AWS Lambda, Python, Boto3, and IAM.

The Lambda function discovers the S3 buckets in my AWS account and checks their security configurations.

## Architecture

AWS Lambda  
↓  
Python + Boto3  
↓  
IAM Execution Role  
↓  
Amazon S3  
↓  
Security Configuration Checks

## Security Checks

- [x] List all S3 buckets
- [x] Check S3 Public Access Block
- [x] Retrieve bucket encryption configuration
- [ ] Analyze encryption algorithm
- [ ] Check bucket versioning
- [ ] Add exception handling
- [ ] Generate final security report

## What I Learned

### Boto3 and S3

I used Boto3 to create an S3 client:

```python
s3 = boto3.client("s3")
