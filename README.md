Red Hat Subscription
=========
[![Galaxy](https://img.shields.io/badge/galaxy-samdoran.redhat--subscription-blue.svg?style=flat)](https://galaxy.ansible.com/samdoran/redhat-subscription)

Manage Red Hat subscritions and repositories.

Requirements
------------

Current Red Hat subscription.

Role Variables
--------------

| Name              | Default Value       | Description          |
|-------------------|---------------------|----------------------|
| `rhsm_username` | No default | Red Hat Portal username. |
| `rhsm_password` | No default | Red Hat Portal password. |
| `rhsm_activation_key` | No default | Red Hat Portal Activation Key. |
| `rhsm_org_id` | No default | Red Hat Portal Organization Identifier. |
| `rhsm_method` | `portal` | Set to `portal` or `satellite` depending on where you are registering. |
| `rhsm_state` | `enable` | Whether to enable or disable a Red Hat subscription. |
| `rhsm_autosubscribe` | `yes` | Whether or not to autosubscibe to available repositories. |
| `rhsm_repos` | `[]` | The list of repositories to enable or disable. See `defaults/main.yml` for examples. |

Dependencies
------------

None.

Example Playbook
----------------

    - hosts: all

      vars:
        rhsm_username: bob.smith@acme.com
        rhsm_password: "{{ vault_rhsm_password }}"
        rhsm_repos:
          - name: rhel-7-server-extras-rpms
            state: present
          - rhel-7-server-rh-common-rpms
          - rhel-7-server-openstack-8-rpms

      roles:
         - samdoran.redhat-subscription

License
-------

Apache 2.0

