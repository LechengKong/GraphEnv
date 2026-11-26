"""Print temporary AWS credentials from the current profile as shell exports (for agent runs)."""
import boto3
c = boto3.Session().get_credentials().get_frozen_credentials()
print(f"export AWS_ACCESS_KEY_ID={c.access_key}")
print(f"export AWS_SECRET_ACCESS_KEY={c.secret_key}")
if c.token:
    print(f"export AWS_SESSION_TOKEN={c.token}")
