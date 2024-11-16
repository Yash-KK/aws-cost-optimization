# AWS Cost Optimization: Automated EBS Snapshot Cleanup

This project aims to reduce AWS costs by automatically identifying and deleting unused Amazon EBS snapshots.
By using an AWS Lambda function triggered on a scheduled basis, we identify and delete snapshots associated with non-existent or unattached EBS volumes, ensuring optimal storage utilization and minimizing unnecessary expenses.

## Features

- **Automated EBS Snapshot Deletion**: Checks snapshots against their volumes to delete those that are unused or no longer needed.
- **Cost Optimization**: Reduces storage costs associated with retaining snapshots of deleted or detached volumes.

## How It Works

1. The Lambda function fetches all snapshots owned by the AWS account.
2. For each snapshot, it verifies:
   - If the volume associated with the snapshot still exists.
   - If the volume exists, it checks if it is attached to any EC2 instance.
3. Snapshots associated with non-existent volumes, or with volumes that are not attached to any EC2 instance, are deleted.
4. This process **can be run** at scheduled intervals using **CloudWatch** to keep storage usage and costs under control.

## Prerequisites

- An AWS account with permissions to create and manage Lambda functions, EC2, and CloudWatch Events.

## Permissions

The Lambda function’s IAM role needs specific permissions to manage snapshots, describe volumes, and delete snapshots. Here is a summary of required permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeSnapshots",
                "ec2:DescribeVolumes",
                "ec2:DeleteSnapshot"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
```
## Setup and Deployment

### Step 1: Create and Configure Lambda Function

1. Go to **AWS Lambda** in the **AWS Console** and create a new Lambda function.
2. Copy the Python code from `lambda_function.py` and paste it into the Lambda code editor.
3. Attach the necessary **IAM role** to your Lambda function, ensuring it has the required permissions (see above).
4. Once the code is pasted, click **Deploy** to save the function.
5. After deploying, click **Test** to run the function and verify it works as expected.

### Step 2: Schedule the Function Using CloudWatch

1. Go to the **CloudWatch Console** > **Rules** > **Create rule**.
2. Under **Event Source**, select **Schedule** and set the desired schedule (e.g., daily or weekly).
3. Under **Targets**, select your Lambda function.
4. Click **Save** to create the rule and schedule the cleanup job.

