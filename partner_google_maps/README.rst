=======================
Partner Google Maps
=======================

This modules allows partners location to be displayed on  Google Map in Odoo.

Installation notes
===================

This Odoo version can not load dynamically Google Maps API from Google site.

The workaround goes as follow:

1. wget https://maps.googleapis.com/maps/api/js?key=<API_KEY>&amp;callback=initMap

2. dump this file in the gapi.js file.

3. repackage and release


Set Google Maps Center, Zoom Level and Google Map API key
---------------------------------------------------------

.. figure:: static/description/Selection_077.png
   :alt: Input Usage
   :scale: 80 %
   :align: center
   :figclass: text-center

.. figure:: static/description/Selection_078.png
   :alt: Input Usage
   :scale: 80 %
   :align: center
   :figclass: text-center

Create a new partner and fill the address
-----------------------------------------
.. figure:: static/description/Selection_079.png
   :alt: Input Usage
   :scale: 80 %
   :align: center
   :figclass: text-center

Select to display partner's map or not
--------------------------------------
.. figure:: static/description/Selection_080.png
   :alt: Input Usage
   :scale: 80 %
   :align: center
   :figclass: text-center

View partner's Google Maps
--------------------------
.. figure:: static/description/Selection_081.png
   :alt: Input Usage
   :scale: 80 %
   :align: center
   :figclass: text-center

Credits
=======

Contributors
------------

* Tuan Nguyen<tuannguyen36.vn@gmail.com>
* Paul Ntabuye Butera <paul.n.butera@abakusitsolutions.eu>

Maintainer
-----------

.. image:: http://www.abakusitsolutions.eu/wp-content/themes/abakus/images/logo.gif
   :alt: AbAKUS IT SOLUTIONS
   :target: http://www.abakusitsolutions.eu

This module is maintained by AbAKUS IT SOLUTIONS