# Lab 01 - AWS Lambda Basics

## Objective

Learn how AWS Lambda receives event data and how Python can process that data for a basic security check.

## What I Learned

- How the `lambda_handler(event, context)` function works
- How Lambda receives JSON data through the `event` parameter
- How to extract values from an event using Python dictionaries
- How to use Python conditions inside a Lambda function
- How to test a Lambda function using a custom test event
- How to troubleshoot a `KeyError` caused by an incorrect event structure

## Security Scenario

This Lambda function checks whether MFA is enabled for a simulated user login.

If MFA is disabled:

`Security-alert: User logged in without MFA`

If MFA is enabled:

`Login Approved`

## Files

- `lambda_function.py` - Lambda function
- `test_event.json` - Sample event used to test the function

## AWS Services

- AWS Lambda
- Amazon CloudWatch Logs
