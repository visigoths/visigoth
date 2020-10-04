.. visigoth documentation master file, created by
   sphinx-quickstart on Thurs Jan 2 09:34:27 2020
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

visigoth
========

visigoth is a lightweight python3 library for making visualisations to display data and geospatial information by rendering them as HTML5 or support vector graphics (SVG) files, typically viewed using a web-browser.  If you are looking for information on the western branch of the ancient nomadic tribe of Germanic peoples referred to collectively as the Goths please refer `to the visualtopology wikipedia page <https://en.wikipedia.org/wiki/visualtopology>`_.

Source code for the visigoth library is available `on github <https://github.com/visualtopology/visigoth>`_.

visigoth can be installed via the command: `python3 -m pip install visigoth`

SVG/HTML output is self contained and embeds any required imagery (web fonts can also be embedded if necessary).

The visualisations can contain multiple maps and charts and can be built with interactive features (for example, brushing can be enabled) when exporting to HTML.

:class:`visigoth.Diagram` objects represent a visualisation and are assembled by adding different elements... these can be common elements (for example, text or image: asic building blocks and controls), container elements (for example, sequence or map: elements that contain one or more elements and apply a layout to the contained elements), or map layer elements (for example, geoimport or kde: layers which can be added to a map container to convey geospatial information about an area).

.. toctree::
   :maxdepth: 2 
   :caption: Contents:

   examples
   charts_summary
   map_layer_summary
   containers_summary
   common_summary

   diagram
   diagram_element


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

