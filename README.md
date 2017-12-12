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
| `rhn_username` | `{{ lookup('env', 'RHN_USERNAME') }}` | Red Hat Portal username. |
| `rhn_password` | `{{ lookup('env', 'RHN_PASSWORD') }}` | Red Hat Portal password. |
| `rhsub_state` | `enable` | Whether to enable or disable a Red Hat subscription. |
| `rhsub_autosubscribe` | `yes` | Whether or not to autosubscibe to available repositories. |
| `rhsub_repos` | `[undefined]` | If defined, the list of repositories to enable or disable. See `defaults/main.yml` for examples. |

Dependencies
------------

None.

Example Playbook
----------------

    - hosts: all

      vars:
        rhn_username: bob.smith@acme.com
        rhn_password: "{{ vault_rhn_password }}"
        rhsub_repos:
          - name: rhel-7-server-extras-rpms
            state: present
          - name: rhel-7-server-rh-common-rpms
          - name: rhel-7-server-openstack-8-rpms

      roles:
         - samdoran.redhat-subscription

License
-------

Apache 2.0

