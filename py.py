#!/usr/bin/python
# Ansible modules must always use this shebang

DOCUMENTATION = """
---
module: py.py
short_description: Run arbitrary Python code
description:
  - Use `set_facts(**kwargs)` to set facts
  - Use `set_result(**kwargs)` to set result
options:
  code:
    type: str
    required: True
  locals:
    type: dict
    required: False
    description:
      - Do not template the `code` itself
      - Define whatever you need in your `code` there
"""


def module_entrypoint():
    # https://docs.ansible.com/ansible/latest/dev_guide/developing_program_flow_modules.html#argument-spec
    module_args = {
        "code": {"type": "str", "required": True},
        "locals": {"type": "dict", "required": False, "default": {}},
    }

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    result = {}
    facts = {}
    _globals = {
        "set_result": result.update,
        "set_facts": facts.update,
        **module.params["locals"],
    }

    code_object = compile(module.params["code"], "<string>", "exec")
    exec(code_object, _globals, _globals)  # pylint: disable=exec-used

    result["ansible_facts"] = facts
    module.exit_json(**result)


if __name__ == "__main__":
    # https://github.com/psf/black/issues/1245
    # fmt: off

    # This is turned into an import statement by Ansible's replacer
    #<<INCLUDE_ANSIBLE_MODULE_COMMON>>

    module_entrypoint()
