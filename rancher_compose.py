#!/usr/bin/python

##
# (c) 2016, GeoData, University of Southampton <geodata@soton.ac.uk>
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.
##

import datetime
import os.path



DOCUMENTATION = '''
---
module: rancher_compose
short_description: Run the C(rancher-compose) tool
version_added: "2.0"
author: "Homme Zwaagstra (hrz@geodata.soton.ac.uk)"
description:
  - Run the C(rancher-compose) tool
    U(http://docs.rancher.com/rancher/rancher-compose/). Rancher stacks can be
    created, started, reloaded, stopped and removed using this module. The stack
    to operate on is determined by the C(project_name) option, and defaults to
    the directory in which the playbook resides.  Note that for the purposes of
    this module, the words I(stack) and I(project_name) are synonymous.
options:
  project_dir:
    description:
      - The working directory under which C(rancher-compose) will run
    required: false
    default: The current working directory
  project_name:
    description:
      - The rancher stack to operate on
    required: false
    default: The directory in which the playbook resides
  docker_compose:
    description:
      - The location of the C(docker-compose.yml) file
    required: false
    default: None
  rancher_compose:
    description:
      - The location of the C(rancher-compose.yml) file
    required: false
    default: None
  env_file:
    description:
      - The location of the file containing C(rancher-compose) environment
        variables.
    required: false
    default: None
  url:
    description:
      - The URL of the rancher server (optionally including the port)
    required: false
    default: None
  access_key:
    description:
      - The access key for the environment under which the project being
        operated on resides. If specified C(secret_key) must be valid
    required: false
    default: None
  secret_key:
    description:
      - The secret key associated with C(access_key).  If specified
        C(access_key) must be valid
    required: false
    default: None
  executable:
    description:
      - The location of the C(rancher-compose) binary
    required: false
    default: rancher-compose
  state:
    description:
      - Assert the stacks required state.  I(present) asserts that the stack has
        been created. I(started) asserts that the stack has been started, but
        will not propagate changes in files referenced by C(docker_compose) or
        C(rancher_compose). I(reloaded) asserts that the stack has been started,
        and also propagates changes in files referenced by C(docker_compose) or
        C(rancher_compose). I(restarted) asserts all services in the stack have
        been restarted. I(stopped) asserts all services in the stack have been
        stopped. I(absent) asserts the stack has been removed.
    choices: ['present', 'started', 'reloaded', 'restarted', 'stopped', 'absent']
    default: started
    required: false
requirements:
  - "python >= 2.6"
  - "rancher-compose >= 0.7.4"
'''

EXAMPLES = '''
# Create a stack
- rancher_compose:
    docker_compose: "{{playbook_dir}}/docker-compose.yml"
    url: http://rancher-server:8080
    access_key: 62883FB58840FB83D016
    secret_key: BCZLqYsrmbxnw4jR6e7iy56cb9qViWayq7Yhnw9C
    state: present

# Update a stack
- rancher_compose:
    docker_compose: "{{playbook_dir}}/docker-compose.yml"
    url: http://rancher-server:8080
    access_key: 62883FB58840FB83D016
    secret_key: BCZLqYsrmbxnw4jR6e7iy56cb9qViWayq7Yhnw9C
    state: reloaded

# Delete a stack
- rancher_compose:
    docker_compose: "{{playbook_dir}}/docker-compose.yml"
    url: http://rancher-server:8080
    access_key: 62883FB58840FB83D016
    secret_key: BCZLqYsrmbxnw4jR6e7iy56cb9qViWayq7Yhnw9C
    state: absent

# Start a stack assuming appropriate environment variables have been set (see
# `rancher-compose --help` for details of environment variables).
- rancher_compose:
    state: started

# Start a stack assuming appropriate environment variables are in the file
# `env-vars.txt`
- rancher_compose:
    env_file: ./env-vars.txt
    state: started
'''

RETURN = '''
cmd:
  description: The rancher compose command which was run
  type: list
  sample: ["rancher-compose", "--file", "/path/to/docker-compose.yml", "--url", "http://rancher-server.example.com:8080", "--access-key", "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER", "--secret-key", "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER", "up", "-d", "--upgrade", "--confirm-upgrade", "--pull"
  returned: On success
delta:
  description: How long it took to run C(rancher-compose)
  type: string
  sample: "0:00:00.340076"
  returned: On success
start:
  description: Timestamp of when C(rancher-compose) started
  type: string
  sample: "2016-04-14 10:14:10.230071"
  returned: On success
end:
  description: Timestamp of when C(rancher-compose) completed
  type: string
  sample: "2016-04-14 10:14:10.570147"
  returned: On success
stderr:
  description: Standard error output captured from C(rancher-compose)
  type: string
  sample: ""
  returned: Whenever rancher compose encounters an error
stdout:
  description: Standard output captured from C(rancher-compose)
  type: string
  sample: "time=\"2016-04-14T10:14:10+01:00\" level=info msg=\"Project [test]: Starting project \" \ntime=\"2016-04-14T10:14:10+01:00\" level=info msg=\"[0/3] [beanstalkd]: Starting \" \ntime=\"2016-04-14T10:14:10+01:00\" level=info msg=\"[0/3] [memcached]: Starting \" \ntime=\"2016-04-14T10:14:10+01:00\" level=info msg=\"[0/3] [postgres]: Starting \" \ntime=\"2016-04-14T10:14:10+01:00\" level=info msg=\"[1/3] [postgres]: Started \" \ntime=\"2016-04-14T10:14:10+01:00\" level=info msg=\"[2/3] [beanstalkd]: Started \" \ntime=\"2016-04-14T10:14:10+01:00\" level=info msg=\"[3/3] [memcached]: Started \" "
  returned: Whenever rancher compose generates output
rc:
  description: The exit code returned by C(rancher-compose)
  type: int
  sample: 0
  returned: Whenever rancher compose returns
'''

def main():
    # Declare the module arguments.
    module = AnsibleModule(
        argument_spec = dict(
            project_dir = dict(type='str', default='.'),
            project_name = dict(),
            docker_compose = dict(),
            rancher_compose = dict(),
            env_file = dict(),
            url = dict(),
            access_key = dict(no_log=True),
            secret_key = dict(no_log=True),
            executable = dict(type='str', default='rancher-compose'),
            state = dict(default='started', choices=['present', 'started', 'reloaded', 'restarted', 'stopped', 'absent']),
        ),
        required_together = (
            ['access_key', 'secret_key'],
        ),
    )

    # Define the module arguments.
    project_dir = os.path.abspath(os.path.expanduser(module.params['project_dir']))
    project_name = module.params['project_name']
    docker_compose = module.params['docker_compose']
    rancher_compose = module.params['rancher_compose']
    env_file = module.params['env_file']
    url = module.params['url']
    access_key = module.params['access_key']
    secret_key = module.params['secret_key']
    executable = module.params['executable']
    state = module.params['state']

    # Set the global rancher-compose command line arguments.
    args = [executable]
    if docker_compose:
        args.extend(['--file', docker_compose])
    if project_name:
        args.extend(['--project-name', project_name])
    if rancher_compose:
        args.extend(['--rancher-file', rancher_compose])
    if env_file:
        args.extend(['--env-file', env_file])
    if url:
        args.extend(['--url', url])
    if access_key:
        args.extend(['--access-key', access_key])
    if secret_key:
        args.extend(['--secret-key', secret_key])

    # Set the state related rancher-compose command line arguments.
    if state == 'started':
        args.extend(['up', '-d', '--confirm-upgrade'])
    elif state == 'present':
        args.append('create')
    elif state == 'reloaded':
        args.extend(['up', '-d', '--upgrade', '--confirm-upgrade', '--pull'])
    elif state == 'restarted':
        args.append('restart')
    elif state == 'stopped':
        args.append('stop')
    elif state == 'absent':
        args.extend(['rm', '--force'])

    # Run rancher-compose.
    startd = datetime.datetime.now()
    rc, out, err = module.run_command(args, executable, cwd=project_dir)
    endd = datetime.datetime.now()
    delta = endd - startd

    # STDOUT and STDERR should always be strings.
    if out is None:
        out = ''
        if err is None:
            err = ''

    # Has the state changed?
    changed = True
    if state == 'reloaded' and 'Upgrading' not in out:
        changed = False
    if state == 'present' and 'Creating' not in out:
        changed = False

    # Return the results.
    module.exit_json(
        cmd      = args,
        stdout   = out.rstrip("\r\n"),
        stderr   = err.rstrip("\r\n"),
        rc       = rc,
        start    = str(startd),
        end      = str(endd),
        delta    = str(delta),
        changed  = changed
    )

# import module snippets
from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
