# ansible-rancher-compose

Use [`rancher-compose`](http://docs.rancher.com/rancher/rancher-compose/) from
[Ansible](https://www.ansible.com/).  This repository defines an
[Ansible module](http://docs.ansible.com/ansible/modules.html) called
`rancher_compose` which is designed to allow the management of
[Rancher stacks](http://docs.rancher.com/rancher/concepts/#stacks) in a
[Rancher environment](http://docs.rancher.com/rancher/concepts/#environments).
It does this by invoking the `rancher-compose` tool.

## Installation

Download and save the module file `rancher_compose.py` to a directory Ansible
recognises as being a module library path.  This directory can be:

* The default library path specified by your Ansible installation.

* A path specified by the `--module-path` option to either the `ansible` or
  `ansible-playbook` commands.

* A path defined in the `ANSIBLE_LIBRARY` environment variable.

* A directory called `library` that resides alongside your top level playbooks.

* A directory defined in the `library` parameter within your `ansible.cfg` file.

## Usage

Unless a `docker-compose.yml` file is specified in the `COMPOSE_FILE`
environment variable then `rancher_compose` requires that the `docker_compose`
option point to a `docker-compose.yml` file.  Unless provided by the appropriate
environment variables, the `url`, `access_key` and `secret_key` options must
also be defined.  Note that environment variables can be defined in the file
pointed to by the `env_file` option.

The Rancher stack is manipulated by setting the `state` option
appropriately. e.g.:

```
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
```

## License

GPL version 3

## Contact

Homme Zwaagstra <hrz@geodata.soton.ac.uk>
