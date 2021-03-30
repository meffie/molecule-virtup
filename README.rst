**********************
Molecule VirtUp Plugin
**********************

Molecule VirtUp is designed to allow use of `virt-up`_ for provisioning of
molecule test guests on a `libvirt` based hypervisor.  The `libvirt` hypervisor
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

Documentation
=============

To use this plugin, you'll need to set the ``driver`` and ``platform``
variables in your ``molecule.yml``. Here's a simple example using the
``generic/centos8`` template:

.. code-block:: yaml

   driver:
     name: virtup

   platforms:
     - name: instance
       template: generic/centos8
       memory: 512
       cpus: 1

Authors
=======

Molecule Virt-Up Plugin was created by Michael Meffie based on code from
Molecule.

License
=======

The `MIT`_ License.

.. _`MIT`: https://github.com/meffie/molecule-virtup/blob/master/LICENSE
