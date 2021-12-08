.. _gjgf-format:

gravis JSON Graph Format (gJGF)
###############################



Introduction
============

The package
:doc:`gravis <package_references>`
uses a custom data format called **gravis JSON Graph Format** or short **gJGF**
to define a single graph with optional annotations or to define a collection of such graphs.
It is a text format that is human-readable and based on
`JSON <https://www.json.org>`__
as well as
`JSON Graph Format (JGF) <https://github.com/jsongraph/json-graph-specification>`__.
Files that contain data in this format should end with the extension ``.gjgf``.

The following specification defines **gJGF version 0.1** by extending JGF with
custom metadata properties.
These properties are recognized by gravis and they are translated into visual elements
and their appearance in graph visualizations. For example, node shapes,
sizes and colors can be influenced among many other options.


Motivation
==========

- `JSON <https://www.json.org>`__
  was chosen because it is a well-supported
  text format in Python and JavaScript,
  but also in many other programming languages.
  This means that it is easy to decode ``JSON strings`` into ``language objects``
  or encode ``language objects`` into ``JSON strings`` with built-in functionality.
  For these purposes Python offers a
  `json module <https://docs.python.org/3/library/json.html>`__
  that can be imported, while JavaScript provides a
  `built-in JSON object <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON>`__
  available in its global scope.
  In contrast, other text formats not based on JSON would have required to write
  custom decoder and encoder functions (or parser and generator functions) in both languages,
  which can be a tedious and error-prone task.

- `JSON Graph Format (JGF) <https://github.com/jsongraph/json-graph-specification>`__
  was chosen because it is open to defining custom metadata, which is suitable for
  introducing specific graph annotations as required by this package. Beyond that,
  building on a well-defined existing format seemed more reasonable than inventing
  yet another completely custom one.



Specification
=============

Part 1: Data types specified by JSON
------------------------------------

JSON is specified in two compatible standards
(`RFC 8259 <https://datatracker.ietf.org/doc/html/rfc8259>`__,
`ECMA-404 <https://www.ecma-international.org/publications-and-standards/standards/ecma-404/>`__)
that aim to define the same formal language with a JSON grammar
written in two different formalisms (ABNF, EBNF).
Here is a short summary of the main ingredients of the JSON language:

- A ``value`` can be an ``object``, ``array``, ``number``, ``string`` or one of
  the literal names ``true``, ``false``, or ``null``.
- An ``object`` structure is represented as a pair of curly brackets surrounding zero
  or more name/value pairs.
- An ``array`` structure is represented as a pair of square brackets surrounding zero
  or more values.
- A ``number`` is a sequence of decimal digits with no leading zero.
- A ``string`` is a sequence of Unicode code points wrapped with quotation marks.

These structures are defined in more detail in the official standards.
In the following text, they will be referred to with their name prefixed by JSON.
They have corresponding data types in Python and JavaScript:

.. table::
   :align: center

   ========================================================================== ==================================================================================================================================== ====================================================================================================================================
   `JSON value <https://datatracker.ietf.org/doc/html/rfc8259#section-3>`__   `Python data type <https://docs.python.org/3/library/stdtypes.html>`__                                                               `JavaScript data type <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Grammar_and_types#data_structures_and_types>`__
   ========================================================================== ==================================================================================================================================== ====================================================================================================================================
   `JSON object <https://datatracker.ietf.org/doc/html/rfc8259#section-4>`__  `dict <https://docs.python.org/3/library/stdtypes.html#dict>`__                                                                      `object <https://developer.mozilla.org/en-US/docs/Glossary/Object>`__
   `JSON array <https://datatracker.ietf.org/doc/html/rfc8259#section-5>`__   `list <https://docs.python.org/3/library/stdtypes.html#list>`__                                                                      `array <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Grammar_and_types#array_literals>`__
   `JSON number <https://datatracker.ietf.org/doc/html/rfc8259#section-6>`__  `int <https://docs.python.org/3/library/functions.html#int>`__ or `float <https://docs.python.org/3/library/functions.html#float>`__ `Number <https://developer.mozilla.org/en-US/docs/Glossary/Number>`__
   `JSON string <https://datatracker.ietf.org/doc/html/rfc8259#section-7>`__  `str <https://docs.python.org/3/library/stdtypes.html#str>`__                                                                        `String <https://developer.mozilla.org/en-US/docs/Glossary/String>`__
   `JSON true <https://datatracker.ietf.org/doc/html/rfc8259#section-3>`__    `True <https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values>`__                                                      `true <https://developer.mozilla.org/de/docs/Glossary/Boolean>`__
   `JSON false <https://datatracker.ietf.org/doc/html/rfc8259#section-3>`__   `False <https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values>`__                                                     `false <https://developer.mozilla.org/de/docs/Glossary/Boolean>`__
   ========================================================================== ==================================================================================================================================== ====================================================================================================================================



Part 2: Graph structure specified by JGF
----------------------------------------

`JSON Graph Format (JGF) <https://github.com/jsongraph/json-graph-specification>`__
is a specification for representing graph structures in JSON.
The package :doc:`gravis <package_references>`
adheres to JGF Version 2 (precisely: commit ce5ed40 on February 1, 2021).
Its ingredients are summarized in the following.
Note that some elements are ignored by gravis, which is indicated below and
means that they do not appear as elements in a graph visualization by default:

- A ``JGF`` structure is a ``JSON object``, which can contain a single name/value pair
  from the following two options:

  .. table::
     :align: center

     ========== ================================= ================================================
     Name       Value                             Meaning
     ========== ================================= ================================================
     "graph"    ``graph`` structure (see below)   A single graph
     "graphs"   ``graphs`` structure (see below)  A collection of graphs
     ========== ================================= ================================================

- A ``graphs`` structure is a ``JSON array``, which can contain zero or more
  ``graph`` structures (see below).

- A ``graph`` structure is a ``JSON object``, which can contain following name/value pairs:

  .. table::
     :align: center

     ============ ============================================= ================================================ ========
     Name         Value                                         Meaning                                          Status
     ============ ============================================= ================================================ ========
     "id"         ``JSON string``                               An identifier for the graph                      optional
     "type"       ``JSON string``                               A classification for the graph                   ignored
     "label"      ``JSON string``                               A text label for the graph                       optional
     "directed"   ``JSON false`` or ``JSON true`` (default)     Undirected or directed graph                     optional
     "nodes"      ``nodes`` structure (see below)               Nodes of the graph                               optional
     "edges"      ``edges`` structure (see below)               Edges of the graph                               optional
     "hyperedges" ``JSON array``                                Hyperedges of a hypergraph                       ignored
     "metadata"   ``graph metadata`` (see part 3)               Custom graph annotations defined by gJGF         optional
     ============ ============================================= ================================================ ========

- A ``nodes`` structure is a ``JSON object``, which represents the nodes or vertices of a graph.
  It can contain zero or more name/value pairs of following form:

  .. table::
     :align: center

     ==================================================== ============================== =================== ========
     Name                                                 Value                          Meaning             Status
     ==================================================== ============================== =================== ========
     ``node id`` which is a ``JSON string``               ``node`` structure (see below) A node of the graph optional
     ==================================================== ============================== =================== ========

  Note that a ``node id`` (and therefore a node) is necessarily unique,
  because it appears as name in a ``JSON object``. This allows edges to unambigously refer to
  a certain node as source or target by its unique ``node id``.

- An ``edges`` structure is a ``JSON array``, which represents the edges or links of a graph.
  It can contain zero or more values, where each value is an ``edge`` structure (see below).

  Note that an edge may not be unique, because it can repeatedly appear as
  entry in a ``JSON array``. This allows to define
  `multiedges <https://en.wikipedia.org/wiki/Multiple_edges>`__
  and thereby
  `multigraphs <https://en.wikipedia.org/wiki/Multigraph>`__.

- A ``node`` structure is a ``JSON object``, which represents a single node.
  It can contain following name/value pairs:

  .. table::
     :align: center

     ============ ============================================= ================================================ ========
     Name         Value                                         Meaning                                          Status
     ============ ============================================= ================================================ ========
     "label"      ``JSON string``                               A text label for the node                        optional
     "metadata"   ``node metadata`` (see part 3)                Custom node annotations defined by gJGF          optional
     ============ ============================================= ================================================ ========

- An ``edge`` structure is a ``JSON object``, which represents a single edge.
  It can contain following name/value pairs, some of which are required:

  .. table::
     :align: center

     ============ ============================================= ============================================================= ========
     Name         Value                                         Meaning                                                       Status
     ============ ============================================= ============================================================= ========
     "source"     ``JSON string``                               Source node, needs to be a ``node id`` contained in ``nodes`` required
     "target"     ``JSON string``                               Target node, needs to be a ``node id`` contained in ``nodes`` required
     "relation"   ``JSON string``                               Interaction between source and target                         ignored
     "label"      ``JSON string``                               A text label for the edge                                     optional
     "directed"   ``JSON true`` or ``JSON false``               Whether the edge is directed or undirected                    ignored
     "metadata"   ``edge metadata`` (see part 3)                Custom edge annotations defined by gJGF                       optional
     ============ ============================================= ============================================================= ========

  Note that "label" is missing in JGF Version 2, but was there in previous states and is still
  present in an example, therefore it was included here.

  .. caution::

     This package detects if an edge has a source or target that is not a node id.
     Such an edge is ignored as if it were not part of the given data.
     A message is written to the web console in the browser, which can be inspected
     by developers but will not be visible to regular users.



Part 3: Graph annotation specified by gJGF
------------------------------------------

JGF contains a ``graph`` structure, a ``node`` structure and an
``edge`` structure. Each of them is a ``JSON object``, where one of the allowed
name/value pairs is "metadata"/``JSON object``. In the following, these objects
associated to the "metadata" name will be referred to as ``graph metadata``,
``node metadata`` and ``edge metadata``. They allow to add custom graph, node and
edge annotations, which can modify the appearance of the graph, its nodes and its
edges when visualized. gJGF specifies which annotations are recognized by gravis.
All values are defined as ``JSON string`` or ``JSON number`` as described below,
but for greater flexibility gravis also accepts ``JSON string`` for numerical values
and auto-converts them to numbers.


- A ``graph metadata`` structure is a ``JSON object`` and can contain following
  name/value pairs:

    .. table::
     :align: center

     ===================== ======================== ======================================================================
     Name                  Value                    Meaning
     ===================== ======================== ======================================================================
     "arrow_color"         ``JSON string``          Color of arrows in directed graphs
     "arrow_size"          ``JSON number``          Size of arrows in directed graphs
     "background_color"    ``JSON string``          Background color of graph drawing area
     "node_color"          ``JSON string``          Fill color of nodes
     "node_opacity"        ``JSON number``          Opacity of nodes
     "node_size"           ``JSON number``          Size of nodes (both height and width)
     "node_shape"          ``JSON string``          Shape of nodes: "circle", "rectangle" or "hexagon"
     "node_border_color"   ``JSON string``          Line color of node border
     "node_border_size"    ``JSON number``          Line width of node border
     "node_label_color"    ``JSON string``          Text color of node labels
     "node_label_size"     ``JSON number``          Text size of node labels
     "node_hover"          ``JSON string``          HTML text shown in a pop-up tooltip when hovering over a node
     "node_click"          ``JSON string``          HTML text shown in details area when clicking on a node
     "node_image"          ``JSON string``          Image shown inside nodes: a URL pointing to an image or a data URL
     "node_x"              ``JSON number``          x position to fix each node at, can be released in UI
     "node_y"              ``JSON number``          y position to fix each node at, can be released in UI
     "node_z"              ``JSON number``          z position to fix each node at, can be released in UI, ignored in 2D
     "edge_color"          ``JSON string``          Line color of edges
     "edge_opacity"        ``JSON number``          Opacity of edges
     "edge_size"           ``JSON number``          Line width of edges
     "edge_label_color"    ``JSON string``          Text color of edge labels
     "edge_label_size"     ``JSON number``          Text size of edge labels
     "edge_hover"          ``JSON string``          HTML text shown in a pop-up tooltip when hovering over an edge
     "edge_click"          ``JSON string``          HTML text shown in details area when clicking on an edge
     ===================== ======================== ======================================================================


- A ``node metadata`` structure is a ``JSON object`` and can contain following
  name/value pairs:

     ===================== ======================== ======================================================================
     Name                  Value                    Meaning
     ===================== ======================== ======================================================================
     "color"               ``JSON string``          Fill color of the node
     "opacity"             ``JSON number``          Opacity of the node
     "size"                ``JSON number``          Size of the node
     "shape"               ``JSON string``          Shape of the node: "circle", "rectangle" or "hexagon" 
     "border_color"        ``JSON string``          Line color of node border
     "border_size"         ``JSON number``          Line width of node border
     "label_color"         ``JSON string``          Text color of node label
     "label_size"          ``JSON number``          Text size of node label
     "hover"               ``JSON string``          HTML text shown in a pop-up tooltip when hovering over the node
     "click"               ``JSON string``          HTML text shown in details area when clicking on the node
     "image"               ``JSON string``          Image shown inside the node: a URL pointing to an image or a data URL
     "x"                   ``JSON number``          x position to fix the node at, can be released in UI
     "y"                   ``JSON number``          y position to fix the node at, can be released in UI
     "z"                   ``JSON number``          z position to fix the node at, can be released in UI, ignored in 2D
     ===================== ======================== ======================================================================


- An ``edge metadata`` structure is a ``JSON object`` and can contain following
  name/value pairs:

     ===================== ======================== ======================================================================
     Name                  Value                    Meaning
     ===================== ======================== ======================================================================
     "color"               ``JSON string``          Line color of the edge
     "opacity"             ``JSON number``          Opacity of the edge
     "size"                ``JSON number``          Line width of the edge
     "label_color"         ``JSON string``          Text color of edge label
     "label_size"          ``JSON number``          Text size of edge label
     "hover"               ``JSON string``          HTML text shown in a pop-up tooltip when hovering over the edge
     "click"               ``JSON string``          HTML text shown in details area when clicking on the edge
     ===================== ======================== ======================================================================




Examples
--------

A minimal graph as JSON text in gJGF:

.. code-block:: javascript

   {
     "graph": {
       "directed": false,
       "nodes": {
         "1": {},
         "2": {},
         "3": {}
       },
       "edges": [
         {"source": 1, "target": 2},
         {"source": 2, "target": 3}
       ]
     }
   }


The same graph as Python dict adhering to gJGF:

.. code-block:: Python

  data = {
    'graph': {
      'directed': False,
      'nodes': {
        1: {},
        2: {},
        3: {},
      },
      'edges': [
        {'source': 1, 'target': 2},
        {'source': 2, 'target': 3},
      ]
    }
  }

Further gJGF examples can be found in `a Jupyter notebook <../code/examples/gjgf.html>`__



.. _supported-graph-libraries:

Auto-conversion of external graph objects to gJGF
-------------------------------------------------

This package supports six popular Python graph libraries which are listed below.
More specifically, the plotting functions of this package accept the different
graph objects of these libraries directly as input.
Internally the plotting functions first convert the graph objects
into gJGF and then proceed as if gJGF data was provided by the user.
The responsible conversion functions are located in the
:py:mod:`gravis.convert` module and
can also be accessed by the user, e.g. to inspect the resulting
gJGF object and check whether everything is converted as expected.

- `graph-tool <https://graph-tool.skewed.de/>`__: :py:mod:`gravis.convert.graphtool_to_gjgf`
- `igraph <https://igraph.org/>`__: :py:mod:`gravis.convert.igraph_to_gjgf`
- `NetworKit <https://networkit.github.io/>`__: :py:mod:`gravis.convert.networkit_to_gjgf`
- `NetworkX <https://networkx.github.io/>`__: :py:mod:`gravis.convert.networkx_to_gjgf`
- `Pyntacle <http://pyntacle.css-mendel.it/>`__: :py:mod:`gravis.convert.pyntacle_to_gjgf`
- `SNAP <http://snap.stanford.edu/>`__: :py:mod:`gravis.convert.snap_to_gjgf`


There are also two convenience functions that make conversions easier:

- Single graph from any supported library: :py:mod:`gravis.convert.any_to_gjgf`
- List of multiple graphs from supported libraries: :py:mod:`gravis.convert.multiple_to_gjgf`
