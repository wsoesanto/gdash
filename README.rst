Gluster Dashboard Repository
============================

This project is intended to simplify administrating Gluster File System. This project is based on `gdash <https://github.com/aravindavk/gdash>`_.

This project is on development. Unlike `gdash <https://github.com/aravindavk/gdash>`_ which can use :code:`--host`, this project has not added that feature yet. The reason is there are some implementation from Gluster that errors when use with :code:`--remote-host` (e.g. :code:`gluster --remote-host=X.X.X.X volume gv0 start`).

Version 0.0.a1,

- Admins are able to look at each folder's layout and start volume from the dashboard.

Usage
=====
Just run :code:`sudo gdash` in gdash folder, gdash starts running in port 5000. visit http://localhost:5000 to view gluster volumes of local machine.

Technical details
=================
Python, Python Flask, Backbone.js

Issues
======
For feature requests, issues, suggestions `here <https://github.com/opelhoward/gdash/issues>`__
