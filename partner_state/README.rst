.. |company| replace:: ADHOC SA

.. |company_logo| image:: https://raw.githubusercontent.com/ingadhoc/maintainer-tools/master/resources/adhoc-logo.png
   :alt: ADHOC SA
   :target: https://www.adhoc.com.ar

.. |icon| image:: https://raw.githubusercontent.com/ingadhoc/maintainer-tools/master/resources/adhoc-icon.png

.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=============
Partner State
=============

Add three states for partners: 'Potential', 'Pending Approval' and 'Approved'.
Some information is required so that a partner can be approved. That
information is configured on: Contacts > Configuration > Partner State Fields.

You can also configure on company if you want to use partner state on that
company or not. The state applies to commercial partners (companies and
individuals without a parent company).

Installation
============

To install this module, you need to:

#. Just install module.

Configuration
=============

To configure this module, you need to:

#. Set "Use partner state " in the company.
#. Set the field that you required to approve partner in Contacts > Configuration > Partner State Fields.
#. Set the permition to approve to the user (group "Approve Partners").

Each line of Partner State Fields has these options:

* **Approval?**: the field is required to request the approval.
* **Changes?**: the changes of the field are logged in the chatter. It only
  adds fields: the fields that Odoo already tracks are always logged, with or
  without a line, and for them this option is checked and can not be unchecked.
* **Track?**: if the field changes on an approved or pending partner, the
  partner goes back to Potential. Checking it also checks **Changes?**.
* **Block Edition**: the field can not be edited on an approved or pending
  partner.

The fields that Odoo tracks on contacts by default are Name, Email, Phone,
Related Company, Salesperson, Tax ID and Inlined Complete Address, plus Parent
name and Company Name Entity, that follow the name. Other installed modules can
add more fields (for example, ``base_ux`` adds Active).

Usage
=====

To use this module, you need to:

#. In the partner view clik the button to approve, or potencial to approve.
#. From the partner list, use the actions "Request Approval Partners" and "Approve Partners" to process several partners at once.


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
