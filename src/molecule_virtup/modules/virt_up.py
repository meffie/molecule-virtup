#!/usr/bin/python

# Copyright (c) 2020, Sine Nomine Associates
# BSD 2-Clause License

ANSIBLE_METADATA = {
    'metadata_version': '1.1.',
    'status': ['preview'],
    'supported_by': 'community',
}

DOCUMENTATION = r"""
---
module: virt_up

short_description: Create instances on libvirt hypervisor with virt-builder

description:
  - Create instances with virt-builder, virt-sysprep, and virt-install

requirements:
  - python virt-up
  - python libvirt
  - libguestfs tools
  - qemu-img

options:
  state:
    description:
      - C(up) Create and instance if it does not exist. Creates a template if needed.
      - C(absent) Delete the instance if it exists.
    type: str
    default: up
    choices:
      - up
      - absent

  name:
    description: The instance name.
    required: true
    type: str

  template:
    description: The os template name. See C(virt-up --list-templates). Required for state C(up).
    type: str

  logfile:
    description: Log file destination on hypervisor.
    type: path
    default: $HOME/.cache/virtup.log

author:
  - Michael Meffie (@meffie)
"""

EXAMPLES = r"""
- name: Create instance(s).
  virt_up:
    state: up
    name: myinst
    template: generic-centos-8
  register: virt_up
"""

RETURN = r"""
keys:
  description: ssh key paths
  type: dict
  sample:
    virtup_identity_file: path to virtup managed key on the hypervisor
    molecule_identity_file: path to the molecule managed key

server:
  description: Molecule instance configuration
  type: dict
  sample:
    instance: instance.name
    address: internet address
    user: login username
    port: ssh port
    identity_file: molecule managed ssh key path

remote_identity_file:
  description: fully qualified path of the generated key on the hypervisor
  type: path
"""

import logging
import os
import grp
import pprint

from ansible.module_utils.basic import AnsibleModule
import virt_up

log = logging.getLogger(__name__)
loglevels = {
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'warning': logging.WARNING,
    'warn': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG,
}

def virtup_identity_file(instance):
    return instance.meta['user']['ssh_identity']

def molecule_identity_file(instance):
    molecule_ephemeral_directory = os.environ['MOLECULE_EPHEMERAL_DIRECTORY']
    ssh_identity = os.path.basename(virtup_identity_file(instance))
    return os.path.join(molecule_ephemeral_directory, ssh_identity)

def run_module():
    result = dict(
        changed=False,
    )
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type='str', choices=['up', 'absent'], default='up'),
            name=dict(type='str', required=True),
            template=dict(type='str', default='default'),
            size=dict(type='str', default=None),
            memory=dict(type='int', default=None),
            cpus=dict(type='int', default=1),
            logfile=dict(type='path', default='~/.cache/virtup.log'),
            loglevel=dict(type='str', choices=loglevels.keys(), default='info'),
        ),
        supports_check_mode=False,
    )
    version = virt_up.__version__
    name = module.params['name']
    state = module.params['state']

    logfile = os.path.expanduser(module.params['logfile'])
    if not os.path.exists(os.path.dirname(logfile)):
        os.makedirs(os.path.dirname(logfile))
    logging.basicConfig(
        filename=logfile,
        level=loglevels[module.params['loglevel']],
        format='%(asctime)s %(levelname)s %(message)s')
    log.info("Starting virt_up: version='%s', state='%s', name='%s', template='%s'",
        version, state, name, module.params['template'])

    try:
        log.debug('LIBVIRT_DEFAULT_URI=%s', os.environ['LIBVIRT_DEFAULT_URI'])
    except KeyError:
        log.warning('LIBVIRT_DEFUALT_URI is not set!')
    for g in os.getgroups():
        log.debug('group: %d(%s)', g, grp.getgrgid(g).gr_name)

    if state == 'up':
        if virt_up.Instance.exists(name):
            instance = virt_up.Instance(name)
        else:
            tinstance = virt_up.Instance.build(
                module.params['template'],
                template=module.params['template'],
                prefix='TEMPLATE-',
                size=module.params['size'],
                memory=module.params['memory'],
                vcpus=module.params['cpus'])
            instance = tinstance.clone(
                name,
                memory=module.params['memory'],
                vcpus=module.params['cpus'])
            result['changed'] = True

        instance.start()
        instance.wait_for_port(22) # Wait for boot to complete.
        log.info("Instance '%s' is up.", instance.name)

        # ssh key locations.
        result['keys'] = {
            'virtup': virtup_identity_file(instance),      # path to virt_up managed keys
            'molecule': molecule_identity_file(instance),  # path to molecule managed keys
        }
        # Molecule instance configuration.
        result['server'] = {
            'instance': instance.name,
            'address': instance.address(),
            'user': instance.meta['user']['username'],
            'port': '22',
            'identity_file': result['keys']['molecule'],
        }
    elif state == 'absent':
        if virt_up.Instance.exists(name):
            instance = virt_up.Instance(name)
            instance.delete()
            log.info("Instance '%s' was deleted.", name)
            result['changed'] = True
    else:
        raise ValueError('Invalid state: %s' % state)

    log.debug('result=%s', pprint.pformat(result))
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
