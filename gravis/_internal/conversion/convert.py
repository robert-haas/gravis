"""This is the module :py:mod:`gravis.convert`.

It provides functions to convert graph objects from external libraries to gJGF.
Additionally, it contains functions to convert image files or image URLs to
self-contained data URLs and HTML elements. This allows to generate visualizations
with images inside nodes that do not rely on any external resources.

"""

from ..utils.web import image_to_data_url, image_to_html_element
from . import _internal


def any_to_gjgf(graph):
    """Convert a graph object from a supported library to gJGF.

    Parameters
    ----------
    graph : graph object from a supported library

    Returns
    -------
    gjgf : dict
        Dictionary adhering to
        :doc:`gravis JSON Graph Format (gJGF) <../../format_specification>`
        with "graph" as top level key.

    """
    dtype = str(type(graph)).lower()
    if isinstance(graph, list):
        dtype_inner = str(type(graph[0])).lower()
        if 'networkit' in dtype_inner:
            dtype = dtype_inner
    if 'graph_tool.graph' in dtype:
        gjgf = graphtool_to_gjgf(graph)
    elif 'igraph.graph' in dtype:
        gjgf = igraph_to_gjgf(graph)
    elif 'networkit' in dtype:
        gjgf = networkit_to_gjgf(graph)
    elif 'networkx.classes' in dtype:
        gjgf = networkx_to_gjgf(graph)
    elif 'snap' in dtype:
        gjgf = snap_to_gjgf(graph)
    else:
        message = 'Provided graph is not a graph object of a supported library.'
        raise ValueError(message)
    return gjgf


def multiple_to_gjgf(graphs):
    """Convert multiple graph objects from supported libraries to gJGF.

    Parameters
    ----------
    graphs : list of graph objects from supported libraries
        The list may contain graph objects from different libraries,
        because each of them is converted individually to gJGF with :func:`any_to_gjgf`.

    Returns
    -------
    gjgf : dict
        Dictionary adhering to
        :doc:`gravis JSON Graph Format (gJGF) <../../format_specification>`
        with "graphs" as top level key

    """
    data = []
    for cnt, graph in enumerate(graphs, 1):
        try:
            data.append(any_to_gjgf(graph)['graph'])
        except Exception:
            msg = 'Graph {} of {} could not be converted to gJGF.'.format(cnt, len(graphs))
            raise ValueError(msg)
    gjgf = {'graphs': data}
    return gjgf


def graphtool_to_gjgf(graph):
    """Convert a graph-tool graph object to gJGF.

    Parameters
    ----------
    graph : graph object from graph-tool

    Returns
    -------
    gjgf : dict
        Dictionary adhering to
        :doc:`gravis JSON Graph Format (gJGF) <../../format_specification>`

    Caution
    -------
    0 and 0.0 values are ignored because they represent missing values in graph-tool.
    This can cause problems when such values have the usual meaning of a quantity being zero.

    """
    data, data_graph, data_nodes, data_edges = _internal.prepare_gjgf_dict()

    # 1) Graph properties
    graph_directed = graph.is_directed()
    graph_metadata_dict = {key: graph.graph_properties[key]  # key syntax is necessary
                           for key in graph.graph_properties.keys()}
    _internal.insert_graph_data(data_graph, graph_directed, graph_metadata_dict)

    # 2) Nodes and their properties
    for node_object in graph.vertices():
        node_id = str(node_object)
        node_metadata_dict = {}
        for key, value_array in graph.vertex_properties.items():
            val = value_array[node_object]
            if isinstance(val, (str, int, float)) and val not in ('', 0, 0.0):
                node_metadata_dict[key] = val
        _internal.insert_node_data(data_nodes, node_id, node_metadata_dict)

    # 3) Edges and their properties
    for edge_object in graph.edges():
        edge_source_id = str(edge_object.source())
        edge_target_id = str(edge_object.target())
        edge_metadata_dict = {}
        for key, value_array in graph.edge_properties.items():
            val = value_array[edge_object]
            if val not in ('', 0, 0.0):
                edge_metadata_dict[key] = val
        _internal.insert_edge_data(data_edges, edge_source_id, edge_target_id, edge_metadata_dict)
    return data


def igraph_to_gjgf(graph):
    """Convert an igraph graph object to gJGF.

    Parameters
    ----------
    graph : graph object from igraph

    Returns
    -------
    gjgf : dict
        Dictionary adhering to
        :doc:`gravis JSON Graph Format (gJGF) <../../format_specification>`

    """
    data, data_graph, data_nodes, data_edges = _internal.prepare_gjgf_dict()

    # 1) Graph properties
    graph_directed = graph.is_directed()
    graph_metadata_dict = {attr: graph[attr] for attr in graph.attributes()}
    _internal.insert_graph_data(data_graph, graph_directed, graph_metadata_dict)

    # 2) Nodes and their properties
    for node_object in graph.vs:
        node_id = str(node_object.index)
        node_metadata_dict = {key: val for key, val in node_object.attributes().items()
                              if val is not None}
        _internal.insert_node_data(data_nodes, node_id, node_metadata_dict)

    # 3) Edges and their properties
    for edge_object in graph.es:
        edge_source_id = str(edge_object.source)
        edge_target_id = str(edge_object.target)
        edge_metadata_dict = {key: val for key, val in edge_object.attributes().items()
                              if val is not None}
        _internal.insert_edge_data(data_edges, edge_source_id, edge_target_id, edge_metadata_dict)
    return data


def networkit_to_gjgf(graph):
    """Convert a NetworKit graph object to gJGF.

    Parameters
    ----------
    graph : graph object from NetworKit

    Returns
    -------
    gjgf : dict
        Dictionary adhering to
        :doc:`gravis JSON Graph Format (gJGF) <../../format_specification>`

    """
    # Argument processing
    graph_metadata, node_metadata, edge_metadata = {}, {}, {}
    if isinstance(graph, list):
        if len(graph) >= 2:
            graph_metadata = graph[1]
        if len(graph) >= 3:
            node_metadata = graph[2]
            if isinstance(node_metadata, dict):
                node_metadata = {str(key): val for key, val in node_metadata.items()}
            else:
                node_metadata = {}
        if len(graph) >= 4:
            edge_metadata = graph[3]
            if isinstance(edge_metadata, dict):
                edge_metadata = {str(key): val for key, val in edge_metadata.items()}
            else:
                edge_metadata = {}
        graph = graph[0]

    # Transformation
    data, data_graph, data_nodes, data_edges = _internal.prepare_gjgf_dict()

    # 1) Graph properties
    # Note: graph.getName() was dropped - https://github.com/networkit/networkit/pull/421
    graph_directed = graph.isDirected()
    graph_metadata_dict = graph_metadata
    _internal.insert_graph_data(data_graph, graph_directed, graph_metadata_dict)

    # 2) Nodes and their properties
    def parse_node(node):
        node_id = str(node)
        node_metadata_dict = node_metadata.get(node_id, {})
        _internal.insert_node_data(data_nodes, node_id, node_metadata_dict)

    graph.forNodes(parse_node)

    # 3) Edges and their properties
    def parse_edge(source_node, target_node, edge_weight, edge_id):
        edge_source_id = str(source_node)
        edge_target_id = str(target_node)
        used_edge_id = '({}, {})'.format(edge_source_id, edge_target_id)
        edge_metadata_dict = edge_metadata.get(used_edge_id, {})
        _internal.insert_edge_data(data_edges, edge_source_id, edge_target_id, edge_metadata_dict)

    graph.forEdges(parse_edge)
    return data


def networkx_to_gjgf(graph):
    """Convert a NetworkX graph object to gJGF.

    Parameters
    ----------
    graph : graph object from NetworkX

    Returns
    -------
    gjgf : dict
        Dictionary adhering to
        :doc:`gravis JSON Graph Format (gJGF) <../../format_specification>`

    """
    data, data_graph, data_nodes, data_edges = _internal.prepare_gjgf_dict()

    # 1) Graph properties
    graph_directed = graph.is_directed()
    graph_metadata_dict = {key: val for key, val in graph.graph.items()}
    _internal.insert_graph_data(data_graph, graph_directed, graph_metadata_dict)

    # 2) Nodes and their properties
    for node_object in graph.nodes:
        node_id = str(node_object)
        node_metadata_dict = {key: val for key, val in graph.nodes[node_object].items()}
        _internal.insert_node_data(data_nodes, node_id, node_metadata_dict)

    # 3) Edges and their properties
    for edge_object in graph.edges:
        edge_source_id = str(edge_object[0])
        edge_target_id = str(edge_object[1])
        edge_metadata_dict = {key: val for key, val in graph.edges[edge_object].items()}
        _internal.insert_edge_data(data_edges, edge_source_id, edge_target_id, edge_metadata_dict)
    return data


def pyntacle_to_gjgf(graph):
    """Convert a Pyntacle graph object to gJGF.

    Parameters
    ----------
    graph : graph object from Pyntacle

    Returns
    -------
    gjgf : dict
        Dictionary adhering to
        :doc:`gravis JSON Graph Format (gJGF) <../../format_specification>`

    """
    # Internally it uses igraph objects, therefore the same conversion method can be used
    return igraph_to_gjgf(graph)


def snap_to_gjgf(graph):
    """Convert a SNAP graph object to gJGF.

    Parameters
    ----------
    graph : graph object from SNAP

    Returns
    -------
    gjgf : dict
        Dictionary adhering to
        :doc:`gravis JSON Graph Format (gJGF) <../../format_specification>`

    """
    import snap

    data, data_graph, data_nodes, data_edges = _internal.prepare_gjgf_dict()

    def get_node_attributes_empty(graph, node_id):
        return {}

    def get_node_attributes_filled(graph, node_id):
        node_attr_dict = {}
        int_attribute_vec = snap.TStrV()
        flt_attribute_vec = snap.TStrV()
        str_attribute_vec = snap.TStrV()
        graph.IntAttrNameNI(node_id, int_attribute_vec)
        graph.FltAttrNameNI(node_id, flt_attribute_vec)
        graph.StrAttrNameNI(node_id, str_attribute_vec)
        for int_attr in int_attribute_vec:
            node_attr_dict[int_attr] = graph.GetIntAttrDatN(node_id, int_attr)
        for flt_attr in flt_attribute_vec:
            node_attr_dict[flt_attr] = graph.GetFltAttrDatN(node_id, flt_attr)
        for str_attr in str_attribute_vec:
            node_attr_dict[str_attr] = graph.GetStrAttrDatN(node_id, str_attr)
        return node_attr_dict

    def get_edge_attributes_empty(graph, edge_id):
        return {}

    def get_edge_attributes_filled(graph, edge_id):
        edge_attr_dict = {}
        int_attribute_vec = snap.TStrV()
        flt_attribute_vec = snap.TStrV()
        str_attribute_vec = snap.TStrV()
        graph.IntAttrNameEI(edge_id, int_attribute_vec)
        graph.FltAttrNameEI(edge_id, flt_attribute_vec)
        graph.StrAttrNameEI(edge_id, str_attribute_vec)
        for int_attr in int_attribute_vec:
            edge_attr_dict[int_attr] = graph.GetIntAttrDatE(edge_id, int_attr)
        for flt_attr in flt_attribute_vec:
            edge_attr_dict[flt_attr] = graph.GetFltAttrDatE(edge_id, flt_attr)
        for str_attr in str_attribute_vec:
            edge_attr_dict[str_attr] = graph.GetStrAttrDatE(edge_id, str_attr)
        return edge_attr_dict

    if 'snap.PNEANet' in str(type(graph)):
        get_node_attributes = get_node_attributes_filled
        get_edge_attributes = get_edge_attributes_filled
    else:
        get_node_attributes = get_node_attributes_empty
        get_edge_attributes = get_edge_attributes_empty

    # 1) Graph properties
    _gt = str(type(graph))
    graph_directed = 'snap.PNGraph' in _gt or 'snap.PDirNet' in _gt or 'snap.PNEANet' in _gt
    graph_metadata_dict = {}  # Note: Seems to not be available in SNAP
    _internal.insert_graph_data(data_graph, graph_directed, graph_metadata_dict)

    # 2) Nodes and their properties
    for node_object in graph.Nodes():
        node_id = str(node_object.GetId())
        node_metadata_dict = get_node_attributes(graph, node_object.GetId())
        _internal.insert_node_data(data_nodes, node_id, node_metadata_dict)

    # 3) Edges and their properties
    for edge_object in graph.Edges():
        edge_source_id = str(edge_object.GetSrcNId())
        edge_target_id = str(edge_object.GetDstNId())
        edge_metadata_dict = get_edge_attributes(graph, edge_object.GetId())
        _internal.insert_edge_data(data_edges, edge_source_id, edge_target_id, edge_metadata_dict)
    return data
