import pydevd_pycharm
from ansible.plugins.action.template import ActionModule as TemplateAction


class ActionModule(TemplateAction):
    def run(self, tmp=None, task_vars=None):
        self.task_vars = task_vars or {}
        # Run the original template plugin
        result = super().run(tmp, task_vars)

        # Mask diff output
        self._mask_diff_content(result)
        return result

    def _mask_diff_content(self, result):
        secret_vars = [
            var
            for key, var in self.task_vars.items()
            if key.startswith('SECRET')
        ]
        if not 'diff' in result:
            return
        diffs = result['diff']
        if isinstance(diffs, dict):
            return
        for diff in diffs:
            for secret_var in secret_vars:
                # pydevd_pycharm.settrace('localhost', port=1337, stdoutToServer=True, stderrToServer=True)
                diff["before"] = diff["before"].replace(secret_var, "*"*len(secret_var))
                diff["after"] = diff["after"].replace(secret_var, "*"*len(secret_var))
