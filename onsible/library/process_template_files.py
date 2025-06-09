#!/usr/bin/python
import pydevd_pycharm

from ansible.module_utils.basic import AnsibleModule
import os
import re
import glob


def flatten_path(path, templates_dir):
    # Drops the first subdir after templates_dir and removes .j2 extension
    pattern = re.compile(rf"^{re.escape(templates_dir)}/[^/]+/")
    new_path = pattern.sub('', path)
    return re.sub(r'\.j2$', '', new_path)


def find_files(paths):
    all_files = []
    for path in paths:
        for root, _, files in os.walk(path):
            for name in files:
                all_files.append(os.path.join(root, name))
    return all_files


def main():
    module_args = dict(
        projects=dict(type='list', elements='str', default=[]),
        templates_dir=dict(type='str', required=True),
        deploy_dir=dict(type='str', required=True)
    )
    # pydevd_pycharm.settrace('localhost', port=1337, stdoutToServer=True, stderrToServer=True)

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    projects = module.params['projects']
    templates_dir = module.params['templates_dir']
    deploy_dir = module.params['deploy_dir']

    combined_source_dirs = [os.path.join(templates_dir, b) for b in projects]

    all_file_paths = find_files(combined_source_dirs)

    file_target_map = {}
    for path in all_file_paths:
        target = os.path.join(deploy_dir, flatten_path(path, templates_dir))
        file_target_map[path] = target

    j2_files = {k: v for k, v in file_target_map.items() if k.endswith('.j2')}
    static_files = {k: v for k, v in file_target_map.items() if not k.endswith('.j2')}

    module.exit_json(
        changed=False,
        file_target_map=file_target_map,
        j2_files=j2_files,
        static_files=static_files
    )


if __name__ == '__main__':
    main()
