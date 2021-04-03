**********************
Molecule VirtUp Plugin
**********************

Molecule VirtUp is designed to allow use of `virt-up`_ for provisioning of
molecule test guests on a libvirt based hypervisor.  The libvirt hypervisor
may be local or remote.

See `virt-up`_ for installation instructions.

.. _`virt-up`: https://github.com/meffie/virt-up.git

Requires
========

On the hypervisor (local or remote)

* libvirt based hypervisor
* ssh server and connection credentials if remote
* python virt_up module and dependencies

Supported libvirt providers:

* qemu/KVM
* XEN

Example
=======

To use this plugin, you'll need to set the ``driver`` and ``platform``
variables in your ``molecule.yml``. Here is a example using the
``generic/centos8`` template:

.. code-block:: yaml

   driver:
     name: virtup
     options:
        connection: local
        host: localhost
        port: 22
        python_interpreter: "/usr/bin/python3"
        libvirt_default_uri: "qemu:///session"

   platforms:
     - name: instance
       template: generic/centos8
       memory: 512
       cpus: 1

Environment variables
=====================

VIRTUP_OPTIONS_FILE
  Specifies the path to the external yaml formatted options file.  An external
  driver options yaml file is supported in order to promote driver independent
  molecule scenarios. Options specified in the ``molecule.yml`` take precedent.

  Default: ``~/.config/molecule-virtup.yml``

Options
=======

connection
  The **ansible_connection** type to connect to the hypervisor; ``local`` or ``ssh``.

  Default: local

host
  The **ansible_host** to connect to the hypervisor when the **connection** is ``local``.

  Default: localhost

port
  The **ansible_port** to connect to the hypervisor when the **connection** is ``local``.

  Default: 22

loglevel
  The logging level name. Log messages are written to the syslog on the hypervisor.
  Specify one of: critical, error, warning, warn, info, debug

  Default: info

python_interpreter
  Specifies the **ansible_python_interpreter** on the hypervisor.

  Default: Detected by ansible

libvirt_default_uri
  The libvirt local connection URI when the ``LIBVIRT_DEFAULT_URI`` environment
  variable is **not** present on the hypervisor for the ansible user. This URI should
  be a local connection URI (e.g. not ssh). The connection URI is used by the
  module running on the hypervisor to connect to the local libvirt daemon also
  running on the hypervisor.

  **virt_up** defaults to ``qemu:///session`` when the ``LIBVIRT_DEFAULT_URI``
  environment variable is not set on the hypervisor and the
  **libvirt_default_uri** option is not specified.

  Default: None

Platform parameters
===================

template
  Name of the ``virt-up`` template definition on the hypervisor. See ``virt-up show templates``.

  Aliases: box

  Default: default

size
  Image size expressed as <number><units>, for example 10G.

  Default: set by template definition

memory
  Memory size of virtual machine in Mb. e.g. 2048

  Default: set by template definition

cpus
  Number of virtual cpus, e.g. 1

  Default: set by template definition

Authors
=======

Molecule Virt-Up Plugin was created by Michael Meffie based on code from
Molecule.

License
=======

The `MIT`_ License.

.. _`MIT`: https://github.com/meffie/molecule-virtup/blob/master/LICENSE
