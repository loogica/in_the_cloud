import ansible.playbook

from ansible import utils
from ansible import callbacks
from ansible import inventory

def run_playbook(playbook_file_name, inventory_file_name):
    stats = callbacks.AggregateStats()
    playbook_cb = callbacks.PlaybookCallbacks(verbose=0)
    runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=0)

    pb = ansible.playbook.PlayBook(playbook_file_name,
        inventory=inventory.Inventory(inventory_file_name),
        callbacks=playbook_cb,
        runner_callbacks=runner_cb,
        stats=stats)

    pb.run()
