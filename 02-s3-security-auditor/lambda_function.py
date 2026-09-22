import boto3

def lambda_handler(event, context):

    # Create S3 client
    s3 = boto3.client("s3")

    # Get all S3 buckets
    response = s3.list_buckets()
    buckets = response["Buckets"]

    # Check each bucket
    for bucket in buckets:

        bucket_name = bucket["Name"]

        print("\n==============================")
        print(f"Bucket Name: {bucket_name}")
        print("==============================")

        # --------------------------------
        # 1. PUBLIC ACCESS BLOCK CHECK
        # --------------------------------
        try:
            public_access = s3.get_public_access_block(
                Bucket=bucket_name
            )

            config = public_access["PublicAccessBlockConfiguration"]

            if (
                config["BlockPublicAcls"]
                and config["IgnorePublicAcls"]
                and config["BlockPublicPolicy"]
                and config["RestrictPublicBuckets"]
            ):
                print("Public Access Block: Secure ✅")
            else:
                print("Public Access Block: Not Secure 🚨")

        except Exception as e:
            print(f"Public Access check failed: {e}")


        # --------------------------------
        # 2. ENCRYPTION CHECK
        # --------------------------------
        try:
            encryption = s3.get_bucket_encryption(
                Bucket=bucket_name
            )

            encryption_config = encryption[
                "ServerSideEncryptionConfiguration"
            ]

            config_rules = encryption_config["Rules"]

            rules_value = config_rules[0]

            encryption_default = rules_value[
                "ApplyServerSideEncryptionByDefault"
            ]

            algorithm = encryption_default["SSEAlgorithm"]

            bucket_key_enabled = rules_value.get(
                "BucketKeyEnabled"
            )

            print(f"Encryption: Enabled ✅")
            print(f"Encryption Algorithm: {algorithm}")
            print(f"Bucket Key Enabled: {bucket_key_enabled}")

        except Exception as e:
            print(f"Encryption check failed: {e}")


        # --------------------------------
        # 3. VERSIONING CHECK
        # --------------------------------
        try:
            versioning = s3.get_bucket_versioning(
                Bucket=bucket_name
            )

            # Status may not exist if versioning
            # has never been enabled
            version_status = versioning.get("Status")

            if version_status == "Enabled":
                print("Versioning: Enabled ✅")

            elif version_status == "Suspended":
                print("Versioning: Suspended ⚠️")

            else:
                print("Versioning: Not Enabled 🚨")

        except Exception as e:
            print(f"Versioning check failed: {e}")
