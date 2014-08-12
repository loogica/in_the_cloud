import os
import sys
import time

import boto.ec2
import paramiko

from decouple import config

SSH_USER = config('SSH_USER')
PASS = config('KEY_PASS')
DEFAULT_INSTANCE_ID = config('DEFAULT_INSTANCE_ID')
DEFAULT_PRIV_KEY = paramiko.RSAKey.from_private_key_file(
    os.path.join(os.path.expanduser('~'), '.ssh/id_rsa'), PASS)

if config('PARAMIKO_DEBUG', cast=bool):
    paramiko.util.log_to_file("paramiko.log")

def connection(region, key_id, access_key):
    conn = boto.ec2.connect_to_region(region, aws_access_key_id=key_id,
                                              aws_secret_access_key=access_key)
    return conn

def run_instance(conn, key_name, _type, sec_group,
                 instance_id=DEFAULT_INSTANCE_ID):
    reservation = conn.run_instances(instance_id,
                                     key_name=key_name,
                                     instance_type=_type,
                                     security_groups=sec_group)

    instance = reservation.instances[0]
    while instance.state != u'running':
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(2)
        instance.update()

    return instance

def gen_inventory_file(inventory_file_name, instance):
    with open(inventory_file_name, 'w+') as config:
        config.write('[mlworker]\n')
        config.write(instance.public_dns_name)


class ComputeInstance(object):
    def __init__(self, instance):
        self.aws_instance = instance
        self.s = paramiko.SSHClient()
        self.s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print('\nConnecting: {}'.format(instance.public_dns_name))
        retry = True
        while retry:
            try:
                sys.stdout.write('.')
                sys.stdout.flush()
                self.s.connect(instance.public_dns_name, 22,
                               username=SSH_USER, pkey=DEFAULT_PRIV_KEY,
                               timeout=2)
            except:
                retry = True
                time.sleep(2)
            else:
                retry = False

        self.sftp = self.s.open_sftp()

    def stop(self):
        self.aws_instance.stop()
        self.s.close()

    def put(self, source, target):
        print("$ local:{} -> remote:{}".format(source, target))
        self.sftp.put(source, target)

    def run(self, command):
        print("\n$ {}".format(command))
        try:
            stdin , stdout, stderr = self.s.exec_command(command)
            out = stdout.read()
            err = stderr.read()
        except:
            print("error:")
        else:
            print("$ <- {}".format(out))
            return out, err

    def send_run(self, source):
        remote_path = source
        self.put(source, remote_path)
        self.run("python {}".format(remote_path))

    @property
    def public_dns_name(self):
        return self.aws_instance.public_dns_name



