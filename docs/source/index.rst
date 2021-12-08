gravis
######

Welcome! You have found the documentation of the Python 3 package
:doc:`gravis <rst/package_references>`.



What is this package?
=====================

Its name stands for graph visualization and its purpose is to create
interactive 2D and 3D plots of
`graphs <https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)>`__
and
`networks <https://en.wikipedia.org/wiki/Network_theory>`__
such as those in following examples:

.. raw:: html

   <p style="margin-left:1em;margin-bottom:1em">
     <a href="code/examples/basic_use.html"><img src="_static/media/basic_use.png" style="height:120px;"></a>
     <a href="code/examples/advanced_use.html"><img src="_static/media/advanced_use.png" style="height:120px;"></a>
     <a href="code/examples/gjgf.html"><img src="_static/media/gjgf.png" style="height:120px;"></a>

     <a href="code/examples/science/biology/human_interactome.html"><img src="_static/media/interactome.png" style="height:120px;"></a>
     <a href="code/examples/science/computer_science/finite_state_machine.html"><img src="_static/media/finite_state_machine.png" style="height:120px;"></a>
     <a href="code/examples/science/international_development/countries.html"><img src="_static/media/countries.png" style="height:120px;"></a>
     <a href="code/examples/science/linguistics/bigrams.html"><img src="_static/media/bigram.png" style="height:120px;"></a>
     <a href="code/examples/science/mathematics/integer_divisors.html"><img src="_static/media/integer_divisors.png" style="height:120px;"></a>
     <a href="code/examples/science/mathematics/modular_arithmetic.html"><img src="_static/media/modular_arithmetic.png" style="height:120px;"></a>
     <a href="code/examples/science/mathematics/stern_brocot_tree.html"><img src="_static/media/stern_brocot.png" style="height:120px;"></a>
     <a href="code/examples/science/social_science/actors_and_movies.html"><img src="_static/media/actors_and_movies.png" style="height:120px;"></a>
     <a href="code/examples/science/social_science/les_miserables.html"><img src="_static/media/les_miserables.png" style="height:120px;"></a>

     <a href="code/examples/external_tools/graph-tool.html"><img src="_static/media/graph-tool.png" style="height:120px;"></a>
     <a href="code/examples/external_tools/igraph.html"><img src="_static/media/igraph.png" style="height:120px;"></a>
     <a href="code/examples/external_tools/networkit.html"><img src="_static/media/networkit.png" style="height:120px;"></a>
     <a href="code/examples/external_tools/networkx.html"><img src="_static/media/networkx.png" style="height:120px;"></a>
     <a href="code/examples/external_tools/pyntacle.html"><img src="_static/media/pyntacle.png" style="height:120px;"></a>
     <a href="code/examples/external_tools/snap.html"><img src="_static/media/snap.png" style="height:120px;"></a>
   </p>

It uses Python for preparing graph data and web technologies (HTML/CSS/JS) for rendering it,
based largely on the JavaScript libraries
`d3.js <https://d3js.org/>`__,
`vis.js <https://visjs.org/>`__
and
`3d-force-graph.js <https://github.com/vasturiano/3d-force-graph>`__ /
`three.js <https://threejs.org/>`__.
The results can either be displayed in a webbrowser window, embedded in a
`Jupyter notebook <https://jupyter.org/>`__, exported to standalone HTML files
or served as HTML text in a web app.
There is also support for exporting static images in JPG, PNG and SVG format,
either by manually clicking a button inside a HTML visualization
or programmatically with
`Selenium <https://selenium-python.readthedocs.io/>`__, which takes a few seconds
to render in a headless browser.

Two types of input data can be passed to the plotting functions:
1) a JSON string or equivalent Python dictionary that encodes a graph
in a custom format called
:doc:`gravis JSON Graph Format (gJGF) <rst/format_specification>` or
2) an external graph object that is automatically translated to gJGF
and may come from the following supported Python packages:
`graph-tool <https://graph-tool.skewed.de/>`__,
`igraph <https://igraph.org/>`__,
`NetworKit <https://networkit.github.io/>`__,
`NetworkX <https://networkx.org/>`__,
`pyntacle <https://pyntacle.css-mendel.it/>`__
and
`SNAP <https://snap.stanford.edu/snap/>`__.



How can it be used?
===================

To get a first impression of the package in action, here is a small code example.
More comprehensive
:doc:`examples <rst/examples/index>`
are available on separate pages.

.. code-block:: python

   import igraph as ig
   import gravis as gv
   import networkx as nx

   graph = {'graph': {'nodes': {'A': {}, 'B': {}}, 'edges': [{'source': 'A', 'target': 'B'}]}}
   fig = gv.vis(graph)
   fig.display()

   graph = nx.powerlaw_cluster_graph(n=120, m=2, p=0.95)
   fig = gv.three(graph)
   fig.export_html('powerlaw_cluster.html')

   graph = ig.Graph.Forest_Fire(120, 0.15)
   fig = gv.d3(graph, zoom_factor=0.25)
   fig.export_svg('forest_fire.svg')

**Results**: `powerlaw_cluster.html <_static/media/powerlaw_cluster.html>`__
and `forest_fire.svg <_static/media/forest_fire.svg>`__

**Interpretation**: The first graph is defined as Python dictionary adhering to gJGF
and displayed in a webbrowser window that opens up automatically.
The second graph is created with the function
`powerlaw_cluster_graph <https://networkx.org/documentation/stable/reference/generated/networkx.generators.random_graphs.powerlaw_cluster_graph.html>`__
from
`NetworkX <https://networkx.org>`__,
internally translated to gJGF and exported as interactive HTML file.
The third graph is created with the function
`Forest_Fire <https://igraph.org/python/api/latest/igraph._igraph.GraphBase.html#Forest_Fire>`__
from
`iGraph <https://igraph.org/python>`__,
also translated to gJGF and exported as static SVG file.



Why is it relevant?
===================

Graphs and networks are studied in various scientific disciplines,
including but not limited to
`mathematics <https://en.wikipedia.org/wiki/Graph_theory>`__,
`computer science <https://en.wikipedia.org/wiki/Computer_network>`__,
`chemistry <https://en.wikipedia.org/wiki/Chemical_reaction_network_theory>`__,
`biology <https://en.wikipedia.org/wiki/Biological_network>`__,
`medicine <https://en.wikipedia.org/wiki/Network_medicine>`__ and
`social science <https://en.wikipedia.org/wiki/Social_network>`__.
Consequently, there is already a range of graph analysis and
visualization software out there, such as the standalone tools
`Gephi <https://gephi.org/>`__,
`Cytoscape <https://cytoscape.org/>`__ or
`Tulip <https://tulip.labri.fr>`__.
This package tries to add some capabilities
to the Python ecosystem by seamlessly connecting it to visualization libraries
from the JavaScript ecosystem, which enables the following features and more:

- Simple creation of **interactive graph visualizations** directly from within Python,
  powered by JavaScript libraries and highly optimized modern webbrowsers.
- Accepting **graph objects from existing Python libraries** as input and auto-converting
  them to a single JSON-based format that can also be provided directly by the user or
  other libraries.
- **Mapping of graph annotations to visual elements** and their appearances,
  revealing much more information than plain connectivities.
- Displaying **images** inside nodes, or in a separate area when hovering or clicking on a node.
- **Flexible layouting** to see substructures within a graph from different perspectives.
  Coordinates can come pre-calculated from external layout algorithms, live-calculated by
  different layouting algorithms running in the browser, or various user interactions such
  as moving and fixing nodes or adjusting force parameters.
- **Easy sharing of results** either by standalone HTML files, Jupyter notebooks with embedded
  graph visualizations that can be exported as a single HTML file, or HTML text that
  can be served in web apps with Python web frameworks such as
  `Flask <https://flask.palletsprojects.com>`__
  and
  `Django <https://www.djangoproject.com/>`__.



When should it be used?
=======================

This package can be used for quickly generating interactive visualizations of
moderately sized graphs (<10000 nodes to be possible, <1000 nodes to be fluid),
which can be directed or undirected and may contain self-loops and multiedges.
There are some scenarios where gravis might be especially useful:

- With its strong support for Jupyter notebooks,
  it is highly suitable for
  `exploratory data analysis <https://en.wikipedia.org/wiki/Exploratory_data_analysis>`__
  and sharing results with others.

- With its capabilities of mapping graph annotations to visual elements,
  it is able to display the results of
  `network analysis algorithms <https://towardsdatascience.com/network-analysis-d734cd7270f8>`__,
  for example by showing
  `network metrics <https://en.wikipedia.org/wiki/Metrics_(networking)>`__
  like
  `centrality values <https://en.wikipedia.org/wiki/Centrality>`__
  in form of node sizes, or by highlighting groups of related nodes found by
  `community detection <https://en.wikipedia.org/wiki/Community_search>`__
  in form of shared node colors.
  An example can be found in the
  `Les Misérables <code/examples/science/social_science/les_miserables.html>`__
  notebook.

- With its support for displaying images inside nodes, it can be used in situations
  where it is necessary to depict graphical information in order to convey
  the meaning of nodes, such as in the case of molecule structures within
  `chemical reaction networks <https://en.wikipedia.org/wiki/Chemical_reaction_network_theory>`__,
  which to a large extent motivated the creation of this package.
  An example can be found in the
  `gJGF <code/examples/gjgf.html>`__
  notebook.

- By allowing users to initially see a whole network, then pan and zoom to interesting regions,
  and finally retrieve detailed information when hovering over or clicking on a node or edge,
  it is possible to build simple information visualization applications that adhere to the
  `visual information-seeking mantra <https://infovis-wiki.net/wiki/Visual_Information-Seeking_Mantra>`__
  by
  `Ben Shneiderman <https://en.wikipedia.org/wiki/Ben_Shneiderman>`__:
  "Overview first, zoom and filter, then details-on-demand".
  An example can be found in the
  `neighboring countries <code/examples/science/international_development/countries.html>`__
  notebook.



Who can benefit from it?
========================

- Users of
  `graph-tool <https://graph-tool.skewed.de>`__,
  `iGraph <https://igraph.org/python>`__,
  `NetworKit <https://networkit.github.io>`__,
  `NetworkX <https://networkx.org>`__,
  `Pyntacle <https://pyntacle.css-mendel.it>`__
  and
  `SNAP <https://snap.stanford.edu>`__
  get a new package for visualizing the graph objects they are already working with.
  Its installation is deliberately kept simple with a single pip command and minimal
  dependencies, so the burden to get started is very low.

- Scientists and technologists working with graphs and networks get
  a rich and flexible way to encode, analyze and visualize them.

- Developers of software that deals with any kind of graph, tree or connectivity data
  can use it for debugging purposes or to add plotting features for their users.

- People without much background knowledge in graph and network theory may get
  interested in these topics by being exposed to visually appealing examples that
  are easy to reproduce and extend.



How can you get started?
========================

- The :doc:`installation guide <rst/installation>`
  explains how to download and install the package and its dependencies.

- The :doc:`examples <rst/examples/index>`
  provide an easy way to get started with using the package.

- The :doc:`API documentation <rst/api/index>` is the single source of truth
  for all details about each available function.



Where is everything located?
============================

The :doc:`package reference page <rst/package_references>`
contains links to all parts of this project, including
source code (with tests, docs, examples),
packaged code (for distribution via PyPI and pip)
and this documentation website.



Table of website contents
=========================

.. toctree::
   :maxdepth: 1

   rst/package_references
   rst/installation
   rst/format_specification
   rst/examples/index
   rst/api/index
