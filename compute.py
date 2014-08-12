from my_ml_cloud import process_unit

with process_unit() as instance:
    instance.send_run('ml.py')
