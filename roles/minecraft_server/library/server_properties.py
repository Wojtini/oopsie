#!/usr/bin/python
from typing import Tuple, List, Any

from ansible.module_utils.basic import AnsibleModule
from pathlib import Path


class ServerProperties:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path
        if not Path(self.file_path).is_file():
            raise Exception(f"File {self.file_path} not found")
        with open(self.file_path, mode="r") as f:
            settings_raw: str = f.read()
        settings_list: list[str] = settings_raw.split("\n")
        self.settings_map: dict[str, str] = {
            key_val[0]: key_val[1]
            for line in settings_list
            if (key_val := self.get_key_value_from_string(line))
        }
        self.changed_keys: List[Tuple[str, str]] = []

    @property
    def changed(self) -> bool:
        return bool(self.changed_keys)

    @staticmethod
    def get_key_value_from_string(s: str) -> Tuple[str, str]:
        splitted = s.split("=")
        if len(splitted) == 1:
            return splitted[0], ""
        if len(splitted) == 2:
            return splitted[0], splitted[1]
        raise Exception("Bad file format")

    def keys(self):
        return self.settings_map.keys()

    def __getitem__(self, item: str):
        return self.settings_map[item]

    def __setitem__(self, key: str, value: Any):
        if key not in self.settings_map:
            raise Exception("No key in settings")

        normalized_value = self._normalize_value(value)
        old_value = self.settings_map[key]
        if old_value == normalized_value:
            return
        self.changed_keys.append((key, f"Changed from [{old_value}] to [{normalized_value}]"))
        self.settings_map[key] = normalized_value

    @staticmethod
    def _normalize_value(value):
        if isinstance(value, bool):
            value = "true" if value else "false"
        elif value is None:
            value = ""
        elif value == "True" or value == "False":
            value = value.lower()
        else:
            value = str(value)
        return value

    def save(self) -> None:
        with open(Path(self.file_path), "w") as f:
            f.write(
                "\n".join(
                    f"{key}={value}" for key, value in self.settings_map.items()
                )
            )


def main() -> None:
    module_args = dict(
        file=dict(type="str", required=True),
        server_settings=dict(type="dict", required=True),
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    if module.check_mode:
        module.exit_json(failed=False, changed=True)

    file = module.params["file"]
    server_settings = module.params["server_settings"]

    sp = ServerProperties(file)

    for key, new_value in server_settings.items():
        sp[key] = new_value

    if sp.changed:
        msg = f"Server properties changed: {sp.changed_keys}"
        sp.save()
    else:
        msg = f"Server properties are up to date"

    module.exit_json(changed=sp.changed, message=msg)


if __name__ == "__main__":
    main()
