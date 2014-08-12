import boto.ec2

from decouple import config

from my_ansible import run_playbook
from my_aws import (connection, run_instance, gen_inventory_file,
                    ComputeInstance)


key_name = config('KEY_NAME')
aws_access_key = config("AWS_ACCESS_KEY")
aws_secret_key = config("AWS_SECRET_KEY")
region = config('REGION')
instance_size = config('INSTANCE_SIZE')
sec_group = config('DEFAULT_SECURITY_GROUP')


def get_instance(conn, instance_id=None):
    if instance_id:
        instances = conn.get_only_instances(instance_ids=[instance_id])
        instance = instances[0]
        instance.start()
        return instance
    else:
        return run_instance(conn, key_name, instance_size, [sec_group])


class process_unit(object):
    def __init__(self, instance_id=None):
        if instance_id:
            raise Exception("Resume created instanced not supported yet")
        self.conn = connection(region, aws_access_key, aws_secret_key)
        self.instance_id = instance_id

    def __enter__(self):
        self.running_instance = get_instance(self.conn,
                                             instance_id=self.instance_id)

        self.running_instance = ComputeInstance(self.running_instance)

        gen_inventory_file('dev.hosts', self.running_instance.aws_instance)
        if not self.instance_id:
            run_playbook('aws_setup_python_env.yml', 'dev.hosts')
            _id = self.running_instance.aws_instance.id
            print("Image Id: {}".format(_id))

        print("Setting up: {}".format(self.running_instance.public_dns_name))
        return self.running_instance

    def __exit__(self, _type, value, traceback):
        self.running_instance.stop()
