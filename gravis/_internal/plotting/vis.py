"""Graph visualization with HTML/CSS/JS based on vis.js."""

from ..conversion import _internal
from ..utils.args import check_arg as _ca
from . import data_structures as _ds
from . import template_system as _ts


def vis(data,
        graph_height=450, details_height=100,
        show_details=False, show_details_toggle_button=True,
        show_menu=False, show_menu_toggle_button=True,
        show_node=True, node_size_factor=1.0,
        node_size_data_source='size', use_node_size_normalization=False,
        node_size_normalization_min=5.0, node_size_normalization_max=75.0,
        node_drag_fix=False, node_hover_neighborhood=False, node_hover_tooltip=True,
        show_node_image=True, node_image_size_factor=1.0,
        show_node_label=True, show_node_label_border=True, node_label_data_source='id',
        node_label_size_factor=1.0, node_label_rotation=0.0, node_label_font='Arial',
        show_edge=True, edge_size_factor=1.0,
        edge_size_data_source='size', use_edge_size_normalization=False,
        edge_size_normalization_min=0.2, edge_size_normalization_max=5.0,
        edge_curvature=0.0, edge_hover_tooltip=True,
        show_edge_label=False, show_edge_label_border=True, edge_label_data_source='id',
        edge_label_size_factor=1.0, edge_label_rotation=0.0, edge_label_font='Arial',
        zoom_factor=0.75, large_graph_threshold=500,
        layout_algorithm_active=True, layout_algorithm='barnesHut',
        gravitational_constant=-2000.0, central_gravity=0.1, spring_length=70.0,
        spring_constant=0.1, avoid_overlap=0.0):
    """Create an interactive graph visualization with HTML/CSS/JS based on vis.js.

    Note
    ----
    This function has some known limitations in comparison to :func:`d3`:

    - vis.js does not support setting the opacity of nodes and edges.
      It also does not support setting arrow colors different from the edge color.
      Accordingly, this functions ignores following properties in the given data:

      - Graph metadata: ``arrow_color``, ``node_opacity``, ``edge_opacity``
      - Node metadata: ``opacity``
      - Edge metadata: ``opacity``

    - Node and edge labels can not be rotated.
    - Node and edge label borders may not be visible if zoomed closely.
    - If edges are hidden, then edge labels are hidden too.
    - Multi-edges are drawn on top of each other and therefore not discernable.
    - Self-loops are drawn as unusual circles that look odd.
    - The initial zoom factor can not be controlled yet.
    - If an image is shown inside a node, its shape is always a rectangle, even if the
      value for node shape desires another choice.
    - Static image export only works in raster image formats JPG and PNG,
      not in vector image format SVG.

    Caution
    -------
    There is a known bug when a node id is chosen to be "x" or "y",
    which seems to clash with internal coordinate calculation.

    Parameters
    ----------
    data : str, dict, graph object, list
        The input data needs to be in a custom format called
        :ref:`gravis JSON Graph Format (gJGF) <gJGF-format>`.

        It can be provided in following ways:

        - *str*: A string in gJGF, or a filepath to a text file in gJGF.
        - *dict*: A dict adhering to gJGF.
        - *graph object*: An object from a
          :ref:`supported graph library <supported-graph-libraries>`,
          which internally gets converted to gJGF.
        - *list*: Instead of a single graph, it is possible to provide a list of graphs.
          They can be all be of the same type, but a mix of different types is also accepted.
          The first graph in the list is shown after the visualization has loaded.
          The other graphs can be chosen in the data selection menu of the
          interactive visualization.
    graph_height : int, float
        Height of the graph container in pixels (px).
    details_height : int, float
        Height of the details container in pixels (px).
    show_details : bool
        If True, the details container is shown on load, otherwise hidden.
    show_details_toggle_button : bool
        If True, a button is shown that allows to toggle the visibility of the details container.
    show_menu : bool
        If True, the menu container is shown on load, otherwise hidden.
    show_menu_toggle_button : bool
        If True, a button is shown that allows to toggle the visibility of the menu container.
    show_node : bool
        If True, nodes are shown on load, otherwise hidden.
    node_size_factor : int, float
        A scaling factor that modifies node size.
    node_size_data_source : str
        Name of the numerical node property that is used as source for node size on load.
    use_node_size_normalization : bool
        If True, node sizes are normalized to lie in an interval between a
        chosen min and max value.
    node_size_normalization_min : int, float
        Minimum value for node size if node size normalization is active.
    node_size_normalization_max : int, float
        Maximum value for node size if node size normalization is active.
    node_drag_fix : bool
        If True, the position of a node becomes fixed after dragging it, i.e. the
        layout algorithm does not change its position but the user can drag it again.
    node_hover_neighborhood : bool
        If True, hovering a node leads to highlighting its neighborhood which consists of
        all incident edges and adjacent nodes.
    node_hover_tooltip : bool
        If True, hovering a node leads to popping up a tooltip if the hover property in the
        metadata of this node contains a non-empty string or HTML text.
    show_node_image : bool
        If True, node images are shown on load for all nodes whose image property in the metadata
        contains a valid image URL from which an image can be fetched.
    node_image_size_factor : int, float
        A scaling factor that modifies node image size.
    show_node_label : bool
        If True, node labels are shown on load, otherwise hidden.
    show_node_label_border : bool
        If True, node labels have a small border in the color of the background to better
        separate the text from other visual elements like edges or nodes.
    node_label_data_source : str
        Name of the node property that is used as source for node label text on load.
    node_label_size_factor : int, float
        A scaling factor that modifies node label size.
    node_label_rotation : int, float
        An angle that modifies node label orientation.
        Caution: This feature is currently ignored in this plot and only here for API consistency.
    node_label_font : str
        Name of the font that is used for node labels.
    show_edge : bool
        If True, edges are shown on load, otherwise hidden.
    edge_size_factor : int, float
        A scaling factor that modifies edge size (=edge width).
    edge_size_data_source : str
        Name of the edge property that is used as source for edge size on load.
    use_edge_size_normalization : bool
        If True, edge sizes are normalized to lie in an interval between a
        chosen min and max value.
    edge_size_normalization_min : int, float
        Minimum value for edge size if node size normalization is active.
    edge_size_normalization_max : int, float
        Maximum value for edge size if node size normalization is active.
    edge_curvature : int, float
        A factor that modifies edge curvature, where 0.0 means straight lines.
    edge_hover_tooltip : bool
        If True, hovering an edge leads to popping up a tooltip if the hover property in the
        metadata of this edge contains a non-empty string or HTML text.
    show_edge_label : bool
        If True, edge labels are shown on load, otherwise hidden.
    show_edge_label_border : bool
        If True, edge labels have a small border in the color of the background to better
        separate the text from other visual elements like edges or nodes.
    edge_label_data_source : str
        Name of the edge property that is used as source for edge label text on load.
    edge_label_size_factor : int, float
        A scaling factor that modifies edge label size.
    edge_label_rotation : int, float
        An angle that modifies edge label orientation.
        Caution: This feature is currently ignored in this plot and only here for API consistency.
    edge_label_font : str
        Name of the font that is used for edge labels.
    zoom_factor : int, float
        Factor that modifies how close the camera is to the drawing area on load.
        Caution: This feature is currently ignored in this plot and only here for API consistency.
    large_graph_threshold : int, float
        Number that determines from when on a graph is considered to be large, which
        means that before visualizing it an initial layout is calculated without moving anything.
        Caution: This feature is currently not available.
    layout_algorithm_active : bool
        If True, the layout algorithm is active on load and leads to movement, otherwise inactive.
    layout_algorithm : str
        Name of the used layout algorithm (vis.js term: "solver" of the "physics simulation").
        Possible values: "barnesHut", "forceAtlas2Based", "repulsion", "hierarchicalRepulsion"
    gravitational_constant : int, float
        Number that determines the strength of the many-body force acting between all pairs of
        nodes. It can be positive to cause attraction or negative (usual case) to cause repulsion.
        Only active if layout_algorithm is "barnesHut" or "forceAtlas2Based".
    central_gravity : int, float
        Number that determines the strength of the centering force that pulls the graph
        towards the center of the coordinate system (0,0) to keep it in the display area.
    spring_length : int, float
        Number that determines the desired distance in the links force (vis.js terminology: edges
        are modeled as "springs") that acts between connected pairs of nodes.
    spring_constant : int, float
        Number that determines the strength of the links force.
    avoid_overlap : int, float
        Number that determines the strength of the collision force that acts between nodes
        if they come too close together.
        Only active if layout_algorithm is "barnesHut", "forceAtlas2Based" or
        "hierarchicalRepulsion".

    Returns
    -------
    A :ref:`Figure <figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://visjs.org
    - https://visjs.github.io/vis-network/docs/network

    """
    # Argument processing
    _ca(graph_height, 'graph_height', (int, float))
    _ca(details_height, 'details_height', (int, float))
    _ca(show_details, 'show_details', bool)
    _ca(show_details_toggle_button, 'show_details_toggle_button', bool)
    _ca(show_menu, 'show_menu', bool)
    _ca(show_menu_toggle_button, 'show_menu_toggle_button', bool)
    _ca(show_node, 'show_node', bool)
    _ca(node_size_factor, 'node_size_factor', (int, float))
    _ca(node_size_data_source, 'node_size_data_source', str)
    _ca(use_node_size_normalization, 'use_node_size_normalization', bool)
    _ca(node_size_normalization_min, 'node_size_normalization_min', (int, float))
    _ca(node_size_normalization_max, 'node_size_normalization_max', (int, float))
    _ca(node_drag_fix, 'node_drag_fix', bool)
    _ca(node_hover_neighborhood, 'node_hover_neighborhood', bool)
    _ca(node_hover_tooltip, 'node_hover_tooltip', bool)
    _ca(show_node_image, 'show_node_image', bool)
    _ca(node_image_size_factor, 'node_image_size_factor', (int, float))
    _ca(show_node_label, 'show_node_label', bool)
    _ca(show_node_label_border, 'show_node_label_border', bool)
    _ca(node_label_data_source, 'node_label_data_source', str)
    _ca(node_label_size_factor, 'node_label_size_factor', (int, float))
    _ca(node_label_rotation, 'node_label_rotation', (int, float))
    _ca(node_label_font, 'node_label_font', str)
    _ca(show_edge, 'show_edge', bool)
    _ca(edge_size_factor, 'edge_size_factor', (int, float))
    _ca(edge_size_data_source, 'edge_size_data_source', str)
    _ca(use_edge_size_normalization, 'use_edge_size_normalization', bool)
    _ca(edge_size_normalization_min, 'edge_size_normalization_min', (int, float))
    _ca(edge_size_normalization_max, 'edge_size_normalization_max', (int, float))
    _ca(edge_curvature, 'edge_curvature', (int, float))
    _ca(edge_hover_tooltip, 'edge_hover_tooltip', bool)
    _ca(show_edge_label, 'show_edge_label', bool)
    _ca(show_edge_label_border, 'show_edge_label_border', bool)
    _ca(edge_label_data_source, 'edge_label_data_source', str)
    _ca(edge_label_size_factor, 'edge_label_size_factor', (int, float))
    _ca(edge_label_rotation, 'edge_label_rotation', (int, float))
    _ca(edge_label_font, 'edge_label_font', str)
    _ca(zoom_factor, 'zoom_factor', (int, float))
    _ca(large_graph_threshold, 'large_graph_threshold', (int, float))
    _ca(layout_algorithm_active, 'layout_algorithm_active', bool)
    _ca(layout_algorithm, 'layout_algorithm', str,
        ['barnesHut', 'forceAtlas2Based', 'repulsion', 'hierarchicalRepulsion'])
    _ca(gravitational_constant, 'gravitational_constant', (int, float))
    _ca(central_gravity, 'central_gravity', (int, float))
    _ca(spring_length, 'spring_length', (int, float))
    _ca(spring_constant, 'spring_constant', (int, float))
    _ca(avoid_overlap, 'avoid_overlap', (int, float))
    data = _internal.normalize_graph_data(data)

    # Transformation
    site_template = _ts.load('templates/vis.html')
    insert_data = {
        'DEFINE_VIS': _ts.load('third_party/vis-network/vis-network.min.def.js'),

        'DATA': _ts.to_json(data),
        'GRAPH_HEIGHT': _ts.to_json(graph_height),
        'DETAILS_HEIGHT': _ts.to_json(details_height),
        'SHOW_DETAILS': _ts.to_json(show_details),
        'SHOW_DETAILS_TOGGLE_BUTTON': _ts.to_json(show_details_toggle_button),
        'SHOW_MENU': _ts.to_json(show_menu),
        'SHOW_MENU_TOGGLE_BUTTON': _ts.to_json(show_menu_toggle_button),

        'SHOW_NODE': _ts.to_json(show_node),
        'NODE_SIZE_FACTOR': _ts.to_json(node_size_factor),
        'NODE_SIZE_DATA_SOURCE': _ts.to_json(node_size_data_source),
        'USE_NODE_SIZE_NORMALIZATION': _ts.to_json(use_node_size_normalization),
        'NODE_SIZE_NORMALIZATION_MIN': _ts.to_json(node_size_normalization_min),
        'NODE_SIZE_NORMALIZATION_MAX': _ts.to_json(node_size_normalization_max),
        'NODE_DRAG_FIX': _ts.to_json(node_drag_fix),
        'NODE_HOVER_NEIGHBORHOOD': _ts.to_json(node_hover_neighborhood),
        'NODE_HOVER_TOOLTIP': _ts.to_json(node_hover_tooltip),

        'SHOW_NODE_IMAGE': _ts.to_json(show_node_image),
        'NODE_IMAGE_SIZE_FACTOR': _ts.to_json(node_image_size_factor),

        'SHOW_NODE_LABEL': _ts.to_json(show_node_label),
        'SHOW_NODE_LABEL_BORDER': _ts.to_json(show_node_label_border),
        'NODE_LABEL_DATA_SOURCE': _ts.to_json(node_label_data_source),
        'NODE_LABEL_SIZE_FACTOR': _ts.to_json(node_label_size_factor),
        'NODE_LABEL_ROTATION': _ts.to_json(node_label_rotation),
        'NODE_LABEL_FONT': _ts.to_json(node_label_font),

        'SHOW_EDGE': _ts.to_json(show_edge),
        'EDGE_SIZE_FACTOR': _ts.to_json(edge_size_factor),
        'EDGE_SIZE_DATA_SOURCE': _ts.to_json(edge_size_data_source),
        'USE_EDGE_SIZE_NORMALIZATION': _ts.to_json(use_edge_size_normalization),
        'EDGE_SIZE_NORMALIZATION_MIN': _ts.to_json(edge_size_normalization_min),
        'EDGE_SIZE_NORMALIZATION_MAX': _ts.to_json(edge_size_normalization_max),
        'EDGE_CURVATURE': _ts.to_json(edge_curvature),
        'EDGE_HOVER_TOOLTIP': _ts.to_json(edge_hover_tooltip),

        'SHOW_EDGE_LABEL': _ts.to_json(show_edge_label),
        'SHOW_EDGE_LABEL_BORDER': _ts.to_json(show_edge_label_border),
        'EDGE_LABEL_DATA_SOURCE': _ts.to_json(edge_label_data_source),
        'EDGE_LABEL_SIZE_FACTOR': _ts.to_json(edge_label_size_factor),
        'EDGE_LABEL_ROTATION': _ts.to_json(edge_label_rotation),
        'EDGE_LABEL_FONT': _ts.to_json(edge_label_font),

        'ZOOM_FACTOR': _ts.to_json(zoom_factor),
        'LARGE_GRAPH_THRESHOLD': _ts.to_json(large_graph_threshold),

        'LAYOUT_ALGORITHM_ACTIVE': _ts.to_json(layout_algorithm_active),
        'LAYOUT_ALGORITHM': _ts.to_json(layout_algorithm),
        'GRAVITATIONLAL_CONSTANT': _ts.to_json(gravitational_constant),
        'CENTRAL_GRAVITY': _ts.to_json(central_gravity),
        'SPRING_LENGTH': _ts.to_json(spring_length),
        'SPRING_CONSTANT': _ts.to_json(spring_constant),
        'AVOID_OVERLAP': _ts.to_json(avoid_overlap),
    }
    site_template = _ts.insert(site_template, insert_data)
    fig = _ds.Figure(site_template)
    return fig
