#!/usr/bin/python
#
# Copyright (c) 2017 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from ansible.module_utils.basic import AnsibleModule
import os
import re
import subprocess

DOCUMENTATION = '''
module: redhat_repos
short_description: Handles repositories for rhel machines
description:
    - Handles repositories for rhel machines
version_added: "2.3"
author: "Karim Boumedhel, @karmab"
notes:
    - This module doesn't handle subscriptions of the machine, only its
repositories requirements:
    - subscription manager and a rhel machine
options:
    repos:
        description:
            - a list of repositories to either add or remove
        required: true
        default: null
    only:
        description:
            - whether the indicated repos should be the only one left to the
system
        required: false
        default: no
    state:
        description:
            - whether the repositories should be made present or absent
        required: false
        default: present
'''

EXAMPLES = '''
- name: Assign Openstack Liberty Repositories
  redhat_repos:
   repos:
     - rhel-7-server-rpms
     - rhel-7-server-rh-common-rpms
     - rhel-7-server-openstack-8-rpms
     - rhel-ha-for-rhel-7-server-rpms
     - rhel-7-server-extras-rpms
'''

RETURN = '''
stdout:
    description: output from subscription-manager
    returned: success, when needed
    type: string
    sample: "Loaded plugins: product-id, refresh-packagekit,
        subscription-manager\n
    Updating Red Hat repositories"
'''


def main():
    argument_spec = {
        "repos": {"required": True, "type": "list"},
        "state": {
            "default": "present",
            "choices": ['present', 'absent'],
            "type": 'str'
        },
        "only": {"default": 'no', "required": False,
                 "type": "str", "choices": ['yes', 'no']},

    }
    module = AnsibleModule(argument_spec=argument_spec)
    repos = module.params['repos']
    state = module.params['state']
    only = module.params['only']

    repo_output = subprocess.check_output(
        'subscription-manager repos --list-enabled'.split(' '))
    curr_repo_list = re.findall("Repo ID:\s+(.+)", repo_output)
    repos_to_install = set(repos).difference(set(curr_repo_list))
    if not repos_to_install:
        if only == 'yes':
            if (len(curr_repo_list) == len(repos)):
                module.exit_json(
                    changed=False,
                    msg="only == true  and all repos are installed")
        else:
            module.exit_json(
                changed=False,
                msg="only == false and all repos installed")

    repos = repos_to_install
    if state == 'present':
        if only == 'yes':
            os.system("subscription-manager repos --disable='*'")
        repos = ' '.join(['--enable=' + repo for repo in repos])
        # result = os.system("subscription-manager repos %s" % repos)
        result = os.popen("subscription-manager repos %s" % repos).read()
        if 'Error' in result:
            module.fail_json(msg=result)
        meta = {'result': result}
        changed = True
        skipped = False
    else:
        repos = ' '.join(['--disable=' + repo for repo in repos])
        result = os.popen("subscription-manager repos %s" % repos).read()
        if 'Error' in result:
            module.fail_json(msg=result)
        meta = {'result': result}
        changed = True
        skipped = False
    module.exit_json(changed=changed, skipped=skipped, meta=meta)

if __name__ == '__main__':
    main()
