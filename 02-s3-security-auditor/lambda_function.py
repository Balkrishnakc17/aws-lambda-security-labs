import boto3
import json
def lambda_handler(event, context):
    # Create a s3 client
    s3 = boto3.client('s3')

    # Get s3 bucket name from the client
    response= s3.list_buckets()
    #Get only S3 bucket name from the response dictionary. 
    buckets=response["Buckets"]
    for i in buckets:
        #Get public Access object for each bucket
       public_access=s3.get_public_access_block(Bucket=i["Name"])
       #Get encryption result for each bucket too
       encryption=s3.get_bucket_encryption(Bucket=i["Name"])
        #Only print the bucket name
       print(f"Bucket Name: {i["Name"]}")
       print(json.dumps(encryption,indent=4,default=str))
       #Only store the public access block configuration
       config=public_access["PublicAccessBlockConfiguration"]
       if config["BlockPublicAcls"] and config["IgnorePublicAcls"] and config["BlockPublicPolicy"] and config["RestrictPublicBuckets"]:
           print(f"Bucket-> {i["Name"]} is Secure ✅ ")

       else:
           print(f"Bucket->{i["Name"]} is not Secure 🚨 ‼️ ")
        

        
            

      

            
