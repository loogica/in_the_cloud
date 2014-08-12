import boto.ec2

import my_ml_cloud

def terminate_all(region):
    aws_access_key = my_ml_cloud.aws_access_key
    aws_secret_key = my_ml_cloud.aws_secret_key

    conn = boto.ec2.connect_to_region(region,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key)

    instances = [i for r in conn.get_all_reservations() for i in r.instances]

    for instance in instances:
        conn.terminate_instances(instance_ids=[instance.id])

if __name__ == "__main__":
    region = my_ml_cloud.region
    terminate_all(region)
