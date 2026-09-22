# Lab 02 - AWS S3 Security Auditor

## Project Overview

In this lab, I built an automated **S3 Security Auditor** using AWS Lambda, Python, Boto3, IAM, JSON, and Amazon S3.

The purpose of this project is to automatically discover S3 buckets in an AWS account and inspect important security configurations instead of manually checking each bucket through the AWS Management Console because it helps to get this important security information for big Cloud Company.

The auditor checks were :

- Public Access Block?
- Server-Side Encryption?
- Encryption Algorithm?
- Bucket Versioning?
- AWS API errors using exception handling apply 

---

## Architecture

```text
AWS Lambda
     |
     v
Python + Boto3
     |
     v
Lambda Execution Role
     |
     v
IAM Authorization
     |
     v
Amazon S3 APIs
     |
     v
S3 Security Configuration
     |
     v
CloudWatch Logs
```

When the Lambda function is invoked, Python uses Boto3 to communicate with Amazon S3 APIs.

The Lambda function does not automatically have permission to access S3. Its permissions are controlled by the IAM execution role attached to the function.

---

## 1. Discovering S3 Buckets

First, I created an S3 client using Boto3:

```python
s3 = boto3.client("s3")
```

Then I retrieved the S3 buckets:

```python
response = s3.list_buckets()
```

The Boto3 response contains a large Python dictionary with different information. For this project, I only needed the bucket list:

```python
buckets = response["Buckets"]
```

I then used a loop to extract each bucket name:

```python
for bucket in buckets:
    bucket_name = bucket["Name"]
```

This helped me understand how AWS API responses use Python dictionaries and lists.

---

## 2. Public Access Block Check

The next step was checking the Public Access Block configuration of every bucket.

I used:

```python
s3.get_public_access_block(Bucket=bucket_name)
```

The response contains four important settings:

```text
BlockPublicAcls
IgnorePublicAcls
BlockPublicPolicy
RestrictPublicBuckets
```

My Lambda checks these values and reports whether the expected Public Access Block protections are enabled.

Example:

```text
Public Access Block: Secure ✅
```

or:

```text
Public Access Block: Not Secure 🚨
```

I also used a test bucket with a different Public Access Block configuration to confirm that the auditor could detect the difference.

---

## 3. Server-Side Encryption Check

Next, I checked the server-side encryption configuration for each bucket.

I used:

```python
s3.get_bucket_encryption(Bucket=bucket_name)
```

The Boto3 response contains nested dictionaries and lists.

I learned how to navigate the response:

```text
ServerSideEncryptionConfiguration
        |
        v
Rules
        |
        v
[0]
        |
        v
ApplyServerSideEncryptionByDefault
        |
        v
SSEAlgorithm
```

For example:

```text
SSEAlgorithm: AES256
```

`AES256` represents Amazon S3 managed server-side encryption (SSE-S3).

This part of the lab helped me understand how to extract useful security information from large AWS API responses.

---

## 4. Bucket Key

The encryption configuration also returned:

```text
BucketKeyEnabled
```

I extracted it using:

```python
bucket_key_enabled = rules_value.get("BucketKeyEnabled")
```

I learned that Bucket Key status should not be confused with whether the bucket itself is encrypted.

The encryption algorithm is the main value I use to identify the bucket's server-side encryption configuration.

---

## 5. Versioning Check

I also checked the versioning configuration of every bucket:

```python
s3.get_bucket_versioning(Bucket=bucket_name)
```

One important thing I learned is that the response may not contain a `Status` key when versioning has never been enabled.

Instead of:

```python
versioning["Status"]
```

I used:

```python
version_status = versioning.get("Status")
```

This allows the program to safely handle a missing `Status` key.

The auditor can identify:

```text
Enabled    -> Versioning Enabled ✅
Suspended  -> Versioning Suspended ⚠️
None       -> Versioning Not Enabled 🚨
```

Versioning is useful as a data-protection and recovery control because previous versions of objects can be retained when objects are changed or deleted.

---

## 6. IAM and Least Privilege

One of the most important lessons from this project was understanding how **Lambda, IAM, and Boto3 work together**.

When I created the Lambda function, AWS created an execution role for it.

The default execution role did not have all the S3 permissions required by my security auditor.

For example, when I first attempted:

```python
s3.list_buckets()
```

I received:

```text
AccessDenied
```

The error showed that the Lambda execution role was not authorized to perform:

```text
s3:ListAllMyBuckets
```

I encountered similar authorization errors while adding additional security checks.

Instead of attaching:

```text
AmazonS3FullAccess
```

I followed the **Principle of Least Privilege**.

I added only the permissions required by the Lambda security auditor.

The project required S3 permissions including:

```text
s3:ListAllMyBuckets
s3:GetBucketPublicAccessBlock
s3:GetEncryptionConfiguration
s3:GetBucketVersioning
```

This helped me understand the authorization flow:

```text
Lambda Function
      |
      v
IAM Execution Role
      |
      v
IAM Policy
      |
      v
Boto3 API Request
      |
      v
AWS Authorization
      |
      v
Amazon S3
```

Boto3 does not automatically have permission to access AWS resources.

When Boto3 runs inside Lambda, the permissions available to the code come from the Lambda execution role.

---

## 7. Exception Handling

AWS API operations can fail because of missing permissions, missing configurations, or other AWS API errors.

Without exception handling, one failed security check could stop the entire audit.

I added separate `try/except` blocks for each security check.

```text
For each bucket:

    Try Public Access Block
        |
        +-- Success -> Analyze configuration
        |
        +-- Error -> Report error

    Try Encryption
        |
        +-- Success -> Analyze encryption
        |
        +-- Error -> Report error

    Try Versioning
        |
        +-- Success -> Analyze versioning
        |
        +-- Error -> Report error
```

This allows the Lambda function to continue performing other checks when one security check fails.

---

## Example Audit Output

```text
==============================
Bucket Name: example-bucket-1
==============================
Public Access Block: Secure ✅
Encryption: Enabled ✅
Encryption Algorithm: AES256
Bucket Key Enabled: True
Versioning: Not Enabled 🚨

==============================
Bucket Name: example-bucket-2
==============================
Public Access Block: Secure ✅
Encryption: Enabled ✅
Encryption Algorithm: AES256
Bucket Key Enabled: False
Versioning: Not Enabled 🚨

==============================
Bucket Name: test-bucket
==============================
Public Access Block: Not Secure 🚨
Encryption: Enabled ✅
Encryption Algorithm: AES256
Bucket Key Enabled: True
Versioning: Not Enabled 🚨
```

---

## What I Learned

During this lab, I learned how to:

1. Create an AWS S3 client using Boto3.
2. Retrieve S3 buckets from an AWS account.
3. Extract bucket names from a Boto3 response.
4. Work with nested Python dictionaries and lists returned by AWS APIs.
5. Loop through multiple AWS resources.
6. Check S3 Public Access Block configurations.
7. Retrieve server-side encryption configurations.
8. Identify the encryption algorithm used by a bucket.
9. Check S3 bucket versioning status.
10. Use `.get()` when an AWS response may not contain a specific key.
11. Handle AWS API failures using exception handling.
12. Understand Lambda execution roles.
13. Troubleshoot IAM `AccessDenied` errors.
14. Apply the Principle of Least Privilege.
15. Use Python and Boto3 for cloud security automation.

---

## Python Skills Used

This project helped me connect Python fundamentals with real AWS cloud security tasks.

| Python Skill | How I Used It |
|---|---|
| Dictionaries | Read Boto3 API responses |
| Lists | Process buckets and configuration rules |
| `for` loops | Scan every S3 bucket |
| `if / elif / else` | Evaluate security configurations |
| `.get()` | Safely retrieve optional AWS response values |
| `try / except` | Handle AWS API failures |
| Functions | Build the Lambda handler |
| Boto3 | Communicate with AWS services |

---

## AWS Services and Technologies

- AWS Lambda
- Amazon S3
- AWS IAM
- Amazon CloudWatch Logs
- Python
- Boto3

---

## Security Concepts Practiced

- Principle of Least Privilege
- IAM roles and policies
- AWS API authorization
- Cloud resource auditing
- S3 Public Access Block
- Encryption at rest
- S3 versioning
- Data protection
- Security automation
- Error handling and troubleshooting

---

## Conclusion

This lab helped me understand how Python can be used for real cloud security automation.

Instead of manually checking every S3 bucket through the AWS Console, I built a Lambda function that uses Boto3 to discover S3 buckets and inspect their security configurations automatically.

The biggest lesson from this project was understanding how different AWS and Python concepts work together:

```text
Python
   +
Boto3
   +
AWS Lambda
   +
IAM Least Privilege
   +
Amazon S3
   =
Automated Cloud Security Auditing
```

This project gave me hands-on experience with AWS security auditing, IAM authorization, Boto3, Lambda, and Python automation.- [ ] Add exception handling
- [ ] Generate final security report

## What I Learned

### Boto3 and S3

I used Boto3 to create an S3 client:

```python
s3 = boto3.client("s3")
