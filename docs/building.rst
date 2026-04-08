Building PDF
============

Inside your ``docs`` folder, run::

  make simplepdf

or for more control::

  sphinx-build -M simplepdf . _build

.. note:: To produce a PDF during your usual HTML build (for example ``make html``), enable
   :ref:`simplepdf_build_parallel` in :doc:`configuration`.
