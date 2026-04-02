Building PDF
============

Inside your ``docs`` folder, run::

  make simplepdf

or for more control::

  sphinx-build -M simplepdf . _build

Building PDF alongside HTML
----------------------------

You can also generate the PDF automatically during your normal HTML build by setting
``simplepdf_build_parallel`` in your ``conf.py``:

.. code-block:: python

   simplepdf_build_parallel = True

Then build as usual::

  make html

The PDF will appear in your HTML output directory alongside the generated HTML files.
A separate ``simplepdf`` build runs as a subprocess concurrently with the HTML build,
so the overall build time is close to whichever build takes longer rather than the sum of both.
