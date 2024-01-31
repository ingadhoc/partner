.. |company| replace:: ADHOC SA

.. |company_logo| image:: https://raw.githubusercontent.com/ingadhoc/maintainer-tools/master/resources/adhoc-logo.png
   :alt: ADHOC SA
   :target: https://www.adhoc.com.ar

.. |icon| image:: https://raw.githubusercontent.com/ingadhoc/maintainer-tools/master/resources/adhoc-icon.png

.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=====================
Partner Internal Code
=====================

This module creates a new field called "Internal Code" in res.partner. Internal Code field must be unique per partner, but it will allow to leave this field empty if desired. It also creates a sequence to populate this new field automatically upon partner creation.


Installation
============

To install this module, you need to:

1. Just install the module.

Configuration
=============

To configure this module, you need to:

1. You can enable/disable or change the default sequence called "partner.internal.code" on sequences menu.

Usage
=====

To use this module, you need to:

1. Set an Internal Code

2. Or leave it empty, then a new code will be automatically assigned by the "partner.internal.code" sequence if enabled.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: http://runbot.adhoc.com.ar/

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/ingadhoc/partner/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------

* |company| |icon|

Contributors
------------

Maintainer
----------

|company_logo|

This module is maintained by the |company|.

To contribute to this module, please visit https://www.adhoc.com.ar.
