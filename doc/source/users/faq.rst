
.. _sardana-faq:

===
FAQ
===

What is the Sardana SCADA system and how do I get an overview over the different components?
--------------------------------------------------------------------------------------------
An overview over the different Sardana components can be found here **<LINK>**. 
The basic Sardana SCADA philosophy can be found :ref:`here <introduction>`.

How do I install Sardana?
-------------------------
The Sardana SCADA system consists of different components which have to be installed:
    
    * Tango_: The control system middleware and tools
    * PyTango_: The Python_ language binding for Tango_
    * Taurus_: The GUI toolkit which is part of Sardana SCADA
    * The Sardana device pool, macro server and tools

The complete sardana installation instructions can be found
:ref:`here <installing>`.

How to work with Taurus_ GUI?
-----------------------------
A user documentation for the Taurus_ GUI application can be found
`here <http://packages.python.org/taurus/>`_.

How to produce your own Taurus_ GUI panel?
-------------------------------------------

The basic philosophy of Taurus_ GUI is to provide automatic GUIs which are
automatically replaced by more and more specific GUIs if these are found.
The documentation how to create a generic panel which can be filled via
selection and cut and paste can be found here **<LINK>**.
A more advanced usage is to create a Taurus_ widget and ingrate it into the
application. Documentation for this approach can be found here **<LINK>**.

How to call procedures?
-----------------------
The central idea of the Sardana SCADA system is to execute procedures centrally.
The execution can be started from either:

    * SPOCK offers a command line interface with commands very similar to SPEC.
      It is documented here **<LINK>**.
    * Procedures can also be executed with a GUI interface the macro executor.
      This GUI interface offering input from the keyboard and the generic
      widgets is documented here **<LINK>**. A macro can be associated with a
      specific GUI interface. This mechanism is documented here **<LINK>**.
    * Procedures can also be executed in specific GUIs and specific Taurus_
      widgets. The API to execute macros from this python code is documented
      here **<LINK>**

How to write procedures?
------------------------
User written procedures are central to the Sardana SCADA system. 
Documentation how to write macros can be found :ref:`here <macros>`. 
Macro writers might also find the following documentation interesting:

    * Documentation on how to debug macros  can be found here **<LINK>**
    * In addition of the strength of the python language macro writers can
      interface with common elements (motors, counters) , call other macros
      and use many utilities provided. The macro API can be found :class:`here <MacroServer.macro.Macro>`.
    * Documentation how to document your macros can be found :ref:`here <macro_documentation>`

How to write scan procedures?
-----------------------------
A very common type of procedure is the *ascan* where some quantity is 
varied while recording some other quantities. Many common types of 
general-purpose scans procedures are already available in Sardana **<LINK>**,
and a simple API is provided for writing more specific ones.

How to adapt SARDANA to your own hardware?
------------------------------------------
Sardana is meant to be interfaced to all types of different hardware with all
types of control systems. For every new hardware item the specific behavior
has to be programmed by writing a controller code. The documentation how to
write Sardana controllers and pseudo controllers can be found here **<LINK>**.
This documentation also includes the API which can be used to interface to
the specific hardware item.

How to add your own file format?
--------------------------------
Documentation how to add your own file format can be found here **<LINK>**.

How to use the standard macros?
-------------------------------
The list of all standard macros and their usage can be found here **<LINK>**.

How to add conditions in macros?
--------------------------------
Executing macros and moving elements can be subject to external conditions 
(for example an interlock). New types of software interlocks can be easily
added to the system and are documented here **<LINK>**.

How to write your own Taurus application?
-----------------------------------------
You have basically two possibilities to write your own Taurus_ application
Start from get General TaurusGUI and create a configuration file. This approach
is documented here **<LINK>**.
Start to write your own Qt application in python starting from the Taurus_ main
window. This approach is documented here **<LINK>**.

Which are the standard Taurus graphical GUI components?
-------------------------------------------------------
A list of all standard Taurus GUI components together with screen shots
and example code can be found here **<LINK>**

How to write your own Taurus widget?
------------------------------------
A tutorial of how to write your own Taurus widget can be found
:ref:`here <screenshots>`.

How to work with the graphical GUI editor?
------------------------------------------
Taurus_ uses the QtDesigner/QtCreator  as a graphical editor. Documentation
about `QtDesigner/QtCreator <http://qt.nokia.com/products/developer-tools/>`_.
The Taurus_ specific parts :ref:`here <taurusqtdesigner-tutorial>`.

What are the minimum software requirements for sardana?
-------------------------------------------------------
Sardana is developed under GNU/Linux, but should run also on Windows and OS-X.
The dependencies for installing Sardana can be found here **<LINK>**.

How to configure the system?
----------------------------
Adding and configuring hardware items on an installation is described 
here **<LINK>**.

How to write your own Taurus schema?
------------------------------------
Taurus is not dependent on Tango. Other control systems or just python modules
can be interfaced to it by writing a schema. This approach is documented
here **<LINK>** and a tutorial can be found here **<LINK>**

What are the interfaces to the macro server and the pool?
---------------------------------------------------------
The low level interfaces to the Sardana Device Pool and the Macro server can
be found here **<LINK>**.

What are the data file formats used in the system and how can I read them?
--------------------------------------------------------------------------
It is easily possible to add your own file format but the standard file formats are documented here:
    
    * The SPEC_ file format is documented here **<LINK>** and here is a list
      of tools to read it **<LINK>**
    * The EDF file format is documented here **<LINK>** and here is a list
      of tools to read it **<LINK>**
    * The NEXUS file format is documented here **<LINK>** and here is a list
      of tools to read it **<LINK>**

What is the file format of the configuration files?
---------------------------------------------------
The configuration files for the Taurus_ GUI are defined here **<LINK>**.

.. _ALBA: http://www.cells.es/
.. _ANKA: http://http://ankaweb.fzk.de/
.. _ELETTRA: http://http://www.elettra.trieste.it/
.. _ESRF: http://www.esrf.eu/
.. _FRMII: http://www.frm2.tum.de/en/index.html
.. _HASYLAB: http://hasylab.desy.de/
.. _MAX-lab: http://www.maxlab.lu.se/maxlab/max4/index.html
.. _SOLEIL: http://www.synchrotron-soleil.fr/


.. _Tango: http://www.tango-controls.org/
.. _PyTango: http://packages.python.org/PyTango/
.. _Taurus: http://packages.python.org/taurus/
.. _QTango: http://www.tango-controls.org/download/index_html#qtango3
.. _Qt: http://qt.nokia.com/products/
.. _PyQt: http://www.riverbankcomputing.co.uk/software/pyqt/
.. _PyQwt: http://pyqwt.sourceforge.net/
.. _Python: http://www.python.org/
.. _IPython: http://ipython.scipy.org/
.. _ATK: http://www.tango-controls.org/Documents/gui/atk/tango-application-toolkit
.. _Qub: http://www.blissgarden.org/projects/qub/
.. _numpy: http://numpy.scipy.org/
.. _SPEC: http://www.certif.com/
.. _EPICS: http://www.aps.anl.gov/epics/