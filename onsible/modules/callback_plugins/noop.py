from ansible.utils.display import Display

from ansible.plugins.callback import CallbackBase

display = Display()

class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'pass_through'
    CALLBACK_NEEDS_WHITELIST = False

    def get_secret_values_from_vars(self, result):
        secrets = set()

        # Check normal task vars
        task_vars = getattr(result, '_task_vars', {})
        for key, value in task_vars.items():
            if key.startswith("SECRET_") and isinstance(value, str):
                secrets.add(value)

        # Optionally, check hostvars
        if hasattr(result, '_host') and hasattr(result._host, 'vars'):
            for key, value in result._host.vars.items():
                if key.startswith("SECRET") and isinstance(value, str):
                    secrets.add(value)

        return secrets

    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host.get_name()
        res = result._result

        changed = res.get('changed', False)
        stdout = res.get('stdout')
        stderr = res.get('stderr')

        if changed:
            display.display(f"[CHANGED] {host}", color='yellow')

        if res["changed"]:
            for r in res['results']:
                display.display(f"[DIFF] {r['before']}", color='yellow')
                display.display(f"[DIFF] {r['after']}", color='yellow')

        if stdout:
            print(stdout)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        stderr = result._result.get('stderr')
        if stderr:
            print(stderr)
        else:
            print("Task failed:", result._result)

    def v2_runner_on_unreachable(self, result):
        display.error(f"Unreachable: {result._result.get('msg')}")

    def v2_runner_on_skipped(self, result):
        ...

    def v2_playbook_on_task_start(self, task, is_conditional):
        ...

    def v2_playbook_on_play_start(self, play):
        print(f"\nPLAY: {play.get_name()}")
