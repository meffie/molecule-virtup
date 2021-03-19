***********************
Molecule Virt-Up Plugin
***********************

Molecule Virt-Up is designed to allow use of `virt-builder` and associated
programs for provisioning of test guests on `libvirt`.

The `libvirt` hypervisor may be running locally or remotely.

Documentation
=============

To use this plugin, you'll need to set the ``driver`` and ``platform``
variables in your ``molecule.yml``. Here's a simple example using the
``generic-centos-8`` template:

.. code-block:: yaml

   driver:
     name: virtup

   platforms:
     - name: instance
       template: generic-centos-8
       memory: 512
       cpus: 1

Authors
=======

Molecule Virt-Up Plugin was created by Michael Meffie based on code from
Molecule.

.. _license:

License
=======

The `MIT`_ License.

.. _`MIT`: https://github.com/ansible/molecule/blob/master/LICENSE
