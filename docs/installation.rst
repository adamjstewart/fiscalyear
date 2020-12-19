Installation
============

``fiscalyear`` has no dependencies, making it simple and easy to install. There are multiple ways to install the ``fiscalyear`` module.


pip
---

The recommended way to install ``fiscalyear`` is with ``pip``.

.. code-block:: console

   $ pip install fiscalyear


The fiscalyear module will now appear with your base Python installation.


Anaconda
--------

You can also install ``fiscalyear`` with the ``conda`` package manager.

.. code-block:: console

   $ conda install -c conda-forge fiscalyear


Spack
-----

If you work in an HPC environment, the `Spack <https://spack.io/>`_ package manager can be used to install ``fiscalyear`` as well.

.. code-block:: console

   $ spack install py-fiscalyear
   $ spack load py-fiscalyear


See the `Spack Documentation <https://spack.readthedocs.io/en/latest/>`_ to get started.


Source
------

If you're up for it, you can also install ``fiscalyear`` from source. Simply clone the repository.

.. code-block:: console

   $ git clone https://github.com/adamjstewart/fiscalyear.git


Now build the module.

.. code-block:: console

   $ python setup.py build


Finally, install the package to somewhere in your ``PYTHONPATH``.

.. code-block:: console

   $ python setup.py install --prefix=/path/to/installation/prefix


Drag-n-Drop
-----------

If you want to vendor ``fiscalyear`` with your Python package, you can always download the `source code <https://github.com/adamjstewart/fiscalyear/blob/master/fiscalyear.py>`_. ``fiscalyear`` is composed of a single file, making it easy to drag-n-drop to your current directory and import.
