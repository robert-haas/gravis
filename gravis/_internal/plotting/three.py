"""Graph visualization with HTML/CSS/JS based on d3-force-graph.js using three.js."""

from ..conversion import _internal
from ..utils.args import check_arg as _ca
from . import data_structures as _ds
from . import template_system as _ts


def three(data,
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
          zoom_factor=0.75, large_graph_threshold=200,
          layout_algorithm_active=True,
          use_many_body_force=True, many_body_force_strength=-70.0,
          many_body_force_theta=0.9,
          use_many_body_force_min_distance=False, many_body_force_min_distance=10.0,
          use_many_body_force_max_distance=False, many_body_force_max_distance=1000.0,
          use_links_force=True, links_force_distance=50.0, links_force_strength=0.5,
          use_x_positioning_force=False, x_positioning_force_strength=0.2,
          use_y_positioning_force=False, y_positioning_force_strength=0.2,
          use_z_positioning_force=False, z_positioning_force_strength=0.2,
          use_centering_force=True):
    """Create an interactive graph visualization with HTML/CSS/JS based on 3d-force-graph.js.

    The library 3d-force-graph.js uses three.js to create a 3d visualization in WebGL,
    hence the name for this function.

    Note
    ----
    This function has some known limitations in comparison to :func:`d3`:

    - Nodes do not have a border. Edges do not come with labels.
      Accordingly, this function ignores following properties in the given data:

      - Graph metadata: ``node_border_color``, ``node_border_size``, ``edge_label_color``,
        ``edge_label_size``
      - Node metadata: ``border_color``, ``border_size``
      - Edge metadata: ``label_color``, ``label_size``

    - Node labels can not be rotated.
    - Edge labels are not available yet.
    - Hovering over a node does not support neighborhood highlighting yet.
    - The initial zoom factor can not be controlled yet.
    - If nodes are hidden, then node labels and node images are hidden too.
    - If an image is shown inside a node, no shape is drawn and therefore any
      value provided for node shape and color is ignored.
    - Static image export only works in raster image formats JPG and PNG,
      not in vector image format SVG.

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
        Caution: This feature is currently ignored in this plot and only here for API consistency.
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
        Caution: This feature is currently ignored in this plot and only here for API consistency.
    show_edge_label_border : bool
        If True, edge labels have a small border in the color of the background to better
        separate the text from other visual elements like edges or nodes.
        Caution: This feature is currently ignored in this plot and only here for API consistency.
    edge_label_data_source : str
        Name of the edge property that is used as source for edge label text on load.
        Caution: This feature is currently ignored in this plot and only here for API consistency.
    edge_label_size_factor : int, float
        A scaling factor that modifies edge label size.
        Caution: This feature is currently ignored in this plot and only here for API consistency.
    edge_label_rotation : int, float
        An angle that modifies edge label orientation.
        Caution: This feature is currently ignored in this plot and only here for API consistency.
    edge_label_font : str
        Name of the font that is used for edge labels.
    zoom_factor : int, float
        Factor that modifies how close the camera is to the drawing area on load.
        Caution: This feature is currently ignored in this plot and only here for API consistency.
    large_graph_threshold : int, float
        Number that determines from when on a network is considered to be large, which
        means that before visualizing it an initial layout is calculated without moving anything.
    layout_algorithm_active : bool
        If True, the layout algorithm is active on load and leads to movement, otherwise inactive.
    use_many_body_force : bool
        If True, many body force is active in the layout algorithm.
        This force acts between any pair of nodes but can be restricted to only act on nodes
        within a certain distance.
    many_body_force_strength : int, float
        Number that determines the strength of the force. It can be positive to cause attraction
        or negative (usual case) to cause repulsion between nodes.
    many_body_force_theta : int, float
        Number that determines the accuracy of the Barnes–Hut approximation of the
        many-body simulation where nodes are grouped instead of treated individually
        to improve performance.
    use_many_body_force_min_distance : bool
        If True, a minimum distance between nodes is used in the many-body force calculation.
        This effectively leads to an upper bound on the strength of the force between any two
        nodes and avoids instability.
    many_body_force_min_distance : int, float
        Number that determines the minimum distance between nodes over which the many-body force
        is active.
    use_many_body_force_max_distance : bool
        If True, a maximum distance between nodes is used in the many-body force calculation.
        This can improve performance but results in a more localized layout.
    many_body_force_max_distance : int, float
        Number that determines the maximum distance between nodes over which the many-body force
        is active.
    use_links_force : bool
        If True, link force is active in the layout algorithm.
        This force acts between pairs of nodes that are connected by an edge. It pushes them
        together or apart in order to come close to a certain distance between connected nodes.
    links_force_distance : int, float
        Number that determines the preferred distance between connected nodes.
    links_force_strength : int, float
        Number that determines the strength of the links force.
    use_collision_force : bool
        If True, collision force is active in the layout algorithm.
        This force treats nodes as circles instead of points and acts on pairs of nodes that
        overlap in order to push them apart.
    collision_force_radius : int, float
        Number that determines the radius of the circle around each node.
    collision_force_strength : int, float
        Number that determines the strength of the force.
    use_x_positioning_force : bool
        If True, x-positioning force is active in the layout algorithm.
        This force modifies the x position of each node towards 0.0, effectively pushing them
        towards the yz-plane.
    x_positioning_force_strength : int, float
        Number that indicates the strength of the force.
    use_y_positioning_force : bool
        This force modifies the y position of each node towards 0.0, effectively pushing them
        towards the xz-plane.
    y_positioning_force_strength : int, float
        Number that indicates the strength of the force.
    use_z_positioning_force : bool
        If True, z-positioning force is active in the layout algorithm.
        This force modifies the z position of each node towards 0.0, effectively pushing them
        towards the xy-plane.
    z_positioning_force_strength : int, float
        Number that indicates the strength of the force.
    use_centering_force : bool
        This force attracts each node towards the center of the coordinate system at (0, 0, 0)
        to keep the graph in the display area. It may lead to unexpected repulsion effects
        if all nodes are fixed and then a single one is released by dragging it.

    Returns
    -------
    A :ref:`Figure <figure>` object that can be used for displaying or exporting the plot.

    References
    ----------
    - https://github.com/vasturiano/3d-force-graph

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
    _ca(use_many_body_force, 'use_many_body_force', bool)
    _ca(many_body_force_strength, 'many_body_force_strength', (int, float))
    _ca(many_body_force_theta, 'many_body_force_theta', (int, float))
    _ca(use_many_body_force_min_distance, 'use_many_body_force_min_distance', bool)
    _ca(many_body_force_min_distance, 'many_body_force_min_distance', (int, float))
    _ca(use_many_body_force_max_distance, 'use_many_body_force_max_distance', bool)
    _ca(many_body_force_max_distance, 'many_body_force_max_distance', (int, float))
    _ca(use_links_force, 'use_links_force', bool)
    _ca(links_force_distance, 'links_force_distance', (int, float))
    _ca(links_force_strength, 'links_force_strength', (int, float))
    _ca(use_x_positioning_force, 'use_x_positioning_force', bool)
    _ca(x_positioning_force_strength, 'x_positioning_force_strength', (int, float))
    _ca(use_y_positioning_force, 'use_y_positioning_force', bool)
    _ca(y_positioning_force_strength, 'y_positioning_force_strength', (int, float))
    _ca(use_z_positioning_force, 'use_z_positioning_force', bool)
    _ca(z_positioning_force_strength, 'z_positioning_force_strength', (int, float))
    _ca(use_centering_force, 'use_centering_force', bool)
    data = _internal.normalize_graph_data(data)

    # Transformation
    site_template = _ts.load('templates/three.html')
    insert_data = {
        'DEFINE_THREE': _ts.load('third_party/three/three.min.def.js'),
        'DEFINE_3D_FORCE_GRAPH': _ts.load('third_party/3d-force-graph/3d-force-graph.min.def.js'),

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
        'USE_MANY_BODY_FORCE': _ts.to_json(use_many_body_force),
        'MANY_BODY_FORCE_STRENGTH': _ts.to_json(many_body_force_strength),
        'MANY_BODY_FORCE_THETA': _ts.to_json(many_body_force_theta),
        'USE_MANY_BODY_FORCE_MIN_DISTANCE': _ts.to_json(
            use_many_body_force_min_distance),
        'MANY_BODY_FORCE_MIN_DISTANCE': _ts.to_json(many_body_force_min_distance),
        'USE_MANY_BODY_FORCE_MAX_DISTANCE': _ts.to_json(
            use_many_body_force_max_distance),
        'MANY_BODY_FORCE_MAX_DISTANCE': _ts.to_json(many_body_force_max_distance),
        'USE_LINKS_FORCE': _ts.to_json(use_links_force),
        'LINKS_FORCE_DISTANCE': _ts.to_json(links_force_distance),
        'LINKS_FORCE_STRENGTH': _ts.to_json(links_force_strength),
        'USE_X_POSITIONING_FORCE': _ts.to_json(use_x_positioning_force),
        'X_POSITIONING_FORCE_STRENGTH': _ts.to_json(x_positioning_force_strength),
        'USE_Y_POSITIONING_FORCE': _ts.to_json(use_y_positioning_force),
        'Y_POSITIONING_FORCE_STRENGTH': _ts.to_json(y_positioning_force_strength),
        'USE_Z_POSITIONING_FORCE': _ts.to_json(use_z_positioning_force),
        'Z_POSITIONING_FORCE_STRENGTH': _ts.to_json(z_positioning_force_strength),
        'USE_CENTERING_FORCE': _ts.to_json(use_centering_force),
    }
    site_template = _ts.insert(site_template, insert_data)
    fig = _ds.Figure(site_template)
    return fig
