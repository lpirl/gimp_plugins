gimp_plugins
============

Put the corresponding file into 
``~/.gimp-2.8/plug-ins/`` to enable a Plug-In per user
or into ``/usr/lib/gimp/2.0/plug-ins/`` to enable them globally.
Path names may vary dedenging on OS and GIMP version.

freecrop
--------

This rather trivial Plug-In is useful for fast and easy extraction
of a lot of non-rectangular parts of images (assign a hotkey ;)).

The Image will be crpped to the selection, all non-selected pixels will
be set transparent and the resulting image will be saved under a random name
(UUID) as PNG.

You will find the Plug-In in the 'File' menu.

before | after
------ | ------
![cat in blanket](freecrop_before.jpg) | ![cat in blanket cropped](freecrop_after.png)
