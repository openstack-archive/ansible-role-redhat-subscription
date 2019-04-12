Red Hat Subscription
====================
[![Galaxy](https://img.shields.io/badge/galaxy-openstack.redhat--subscription-blue.svg?style=flat)](https://galaxy.ansible.com/openstack/redhat-subscription)

Manage Red Hat subscriptions and repositories. This role supports registering to Satellite 5, Satellite 6, or the Red Hat Customer Portal.

Requirements
------------

You will need to have an active Red Hat subscription in order for registration to succeed.

Provide `rhsm_username` and `rhsm_password` _or_ `rhsm_activation_key`. These options are mutually exclusive and providing both will result in a failure. The recommended option is to provide an activation key rather than username and password.

Role Variables
--------------

| Name              | Default Value       | Description          |
|-------------------|---------------------|----------------------|
| `rhsm_method` | `portal` | Method to use for activation: `portal` or `satellite`. If `satellite`, the role will determine the Satellite Server version and take the appropriate registration actions. |
| `rhsm_username` | `[undefined]` | Red Hat Portal username. |
| `rhsm_password` | `[undefined]` | Red Hat Portal password. |
| `rhsm_activation_key` | `[undefined]` | Red Hat Portal Activation Key. |
| `rhsm_org_id` | `[undefined]` | Red Hat Portal Organization Identifier. |
| `rhsm_pool_ids` | `[undefined]` | Red Hat Subscription pool IDs to consume. |
| `rhsm_state` | `present` | Whether to enable or disable a Red Hat subscription. |
| `rhsm_autosubscribe` | `[undefined]` | Whether or not to autosubscribe to available repositories. |
| `rhsm_consumer_hostname` | `[undefined]` | Name of the system to use when registering. Defaults to using the system hostname if undefined. |
| `rhsm_force_register` | `False` | Whether or not to force registration. |
| `rhsm_repos` | `[]` | The list of repositories to enable or disable. |
| `rhsm_repos_state` | `[undefined]` | The state of all repos in `rhsm_repos`. The module default is `enabled`.|
| `rhsm_repos_purge` | `[undefined]` | Whether or not to disable repos not specified in `rhsm_repos`. The module default is `False`. |
| `rhsm_rhsm_port` | `443` | Port to use when connecting to subscription server. |
| `rhsm_server_hostname` | `subscription.rhn.redhat.com` | FQDN of subscription server. |
| `rhsm_server_prefix` | `/subscription` or `/rhsm` | RHS server prefix. `/subscription` when using registering via `portal`, `/rhsm` when registering via `satellite`. |
| `rhsm_insecure` | `False` | Disable certificate validation. |
| `rhsm_ssl_verify_depth` | `3` | Depths certificates should be validated when checking. |
| `rhsm_rhsm_proxy_hostname` | `[undefined]` | FQDN of outbound proxy server. |
| `rhsm_rhsm_proxy_port` | `[undefined]` | Port to use for proxy server. |
| `rhsm_rhsm_proxy_user` | `[undefined]` | Username to use for proxy server. |
| `rhsm_rhsm_proxy_password` | `[undefined]` | Password to use for proxy server. Save this in an Ansible Vault or other secret store. |
| `rhsm_baseurl` | `https://cdn.redhat.com` | Base URL for content. |
| `rhsm_satellite_url` | `[see defaults/main.yml]` | URL of the Satellite server that will be probed to determine the Satellite version. Uses the scheme and hostname of `rhsm_baseurl` by default.  |
| `rhsm_ca_cert_dir` | `/etc/rhsm/ca/` | Server CA certificate directory. |
| `rhsm_product_cert_dir` | `/etc/pki/product` | Product certificate directory. |
| `rhsm_entitlement_cert_dir` | `/etc/pki/entitlement` | Entitlement certificate directory. |
| `rhsm_consumer_cert_dir` | `/etc/pki/consumer` | Consumer certificate directory. |
| `rhsm_manage_repos` | `True` | Manage generation of yum repositories for subscribed content. |
| `rhsm_full_refresh_on_yum` | `False` | Refresh repo files with server overrides on every `yum` command. |
| `rhsm_report_package_profile` | `True` | Whether to report the package profiles to the subscription management service. |
| `rhsm_plugin_dir` | `/usr/share/rhsm-plugins` | Directory to search for subscription manage plugins. |
| `rhsm_plugin_conf_dir` | `/etc/rhsm/pluginconf.d` | Directory to search for plugin configuration files. |
| `rhsm_cert_check_interval` | `240` | Interval in minutes to run certificate check. |
| `rhsm_auto_attach_interval` | `1440` | Interval in minutes to run auto-attach. |
| `rhsm_logging` | [see `defaults/main.yml`] | Logging settings for various RHSM components. |

Dependencies
------------

None.


About repositories
------------------

If you are using an activation key with Satellite, the repositories that are
associated to the subscription are configured in your local instance of Satellite.
You can't specify rhsm_repos parameter if you are using rhsm_activation_key with
Satellite.
Otherwise, when using Portal registration method you can use either rhsm_username and
rhsm_password or activation key and you can use rhsm_repos to select which repos get deployed.


Example Playbook with Red Hat portal
------------------------------------

::

    - hosts: all
      vars:
        rhsm_username: bob.smith@acme.com
        rhsm_password: "{{ vault_rhsm_password }}"
        rhsm_repos:
          - rhel-7-server-rpms
          - rhel-7-server-extras-rpms
          - rhel-7-server-rh-common-rpms
          - rhel-ha-for-rhel-7-server-rpms
      roles:
        - openstack.redhat-subscription

Example Playbook with Satellite 6
---------------------------------

::

    - hosts: all
      vars:
        rhsm_activation_key: "secrete_key"
        rhsm_org_id: "Default_Organization"
        rhsm_server_hostname: "mysatserver.com"
        rhsm_baseurl: "https://mysatserver.com/pulp/repos"
        rhsm_method: satellite
        rhsm_insecure: yes
      roles:
        - openstack.redhat-subscription

Example Playbook to unregister
------------------------------

::

    - hosts: all
      tasks:
        - name: Unregister the node
          include_role:
            name: openstack.redhat-subscription
            tasks_from: unregister

License
-------

Apache 2.0

