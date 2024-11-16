import boto3

# Initialize the Boto3 EC2 client
ec2_client = boto3.client("ec2")


def lambda_handler(event, context):
    # Fetch all snapshots owned by this account
    # Using 'OwnerIds=["self"]' ensures we're only working with snapshots that belong to this account
    snapshots = ec2_client.describe_snapshots(OwnerIds=["self"])["Snapshots"]

    # Loop through each snapshot to examine and potentially delete it
    for snapshot in snapshots:
        snapshot_id = snapshot["SnapshotId"]
        volume_id = snapshot["VolumeId"]

        # Check if the volume associated with this snapshot still exists
        try:
            volume = ec2_client.describe_volumes(VolumeIds=[volume_id])["Volumes"][0]
            volume_exists = True  # If successful, the volume exists
        except IndexError:
            # If an IndexError occurs, it likely means the volume doesn't exist anymore
            volume_exists = False

        # Now determine if the snapshot should be deleted based on volume status
        if volume_exists:
            # If the volume exists, check if it's currently attached to any EC2 instance
            attachments = volume.get("Attachments", [])
            if not attachments:
                # If there are no attachments, it means the volume is not attached to any instance
                # This makes the snapshot eligible for deletion
                print(
                    f"Deleting snapshot {snapshot_id} for volume {volume_id} as it's not attached to any instance."
                )
                delete_snapshot(snapshot_id)  # Delete the snapshot
            else:
                # If the volume has attachments, it's currently in use, so we skip deleting the snapshot
                print(
                    f"Snapshot {snapshot_id} for volume {volume_id} is skipped because the volume is attached to an EC2 instance."
                )
        else:
            # If the volume doesn't exist, we can safely delete the snapshot as it's no longer needed
            print(
                f"Deleting snapshot {snapshot_id} for volume {volume_id} as the volume doesn't exist."
            )
            delete_snapshot(snapshot_id)  # Delete the snapshot


def delete_snapshot(snapshot_id):
    # Attempts to delete the specified snapshot
    try:
        ec2_client.delete_snapshot(SnapshotId=snapshot_id)
        print(f"Successfully deleted snapshot: {snapshot_id}")
    except Exception as e:
        # If an error occurs during deletion, it will be printed for debugging purposes
        print(f"Error deleting snapshot {snapshot_id}: {str(e)}")

