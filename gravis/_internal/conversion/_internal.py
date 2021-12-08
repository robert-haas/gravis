"""Internal functions used by the public conversion functions."""

import json as _json
from collections.abc import Iterable as _Iterable

from ..utils import operating_system as _operating_system
from . import convert as _convert


def normalize_graph_data(data):
    """Get graph data in various forms and convert it to a single, unified form (gJGF).

    Parameters
    ----------
    data : JSON string, filepath, dict, graph object
        Following types of data are recognized:

        - A JSON string in gJGF
        - A dictionary adhering to gJGF
        - A filepath to a JSON file adhering to gJGF
        - A graph object from a supported external library
        - A list of the previous types

    Returns
    -------
    data : list
        A list of graphs in gravis JSON Graph Format (gJGF) without the uppermost 'graph' key

    """
    def raise_error(additional_message=None):
        message = 'The provided data seems not to be in a valid graph format.'
        if additional_message:
            message += ' {}'.format(additional_message)
        raise ValueError(message)

    def filepath_to_json_object(filepath):
        with open(filepath) as file_handle:
            return _json.load(file_handle)

    def json_str_to_json_object(text):
        return _json.loads(text)

    def str_to_json_object(text):
        if _operating_system.is_nonempty_file(text):
            data = filepath_to_json_object(text)
        else:
            try:
                data = json_str_to_json_object(text)
            except Exception:
                message = (
                    'Given data is a string that is neither a filepath nor a valid JSON string.')
                raise ValueError(message)
        return data

    # Case 0: A string that can be a filepath to a text file or a JSON string
    if isinstance(data, str):
        data = str_to_json_object(data)
    # Case 1: Single graph object
    if is_known_graph_object(data):
        data = _convert.any_to_gjgf(data)
        data = [data['graph']]
    # Case 2: Single gJGF dict (with single graph)
    elif isinstance(data, dict) and 'graph' in data:
        data = data['graph']
        data = [data]
    # Case 3: Single gJGF dict (with multiple graphs)
    elif isinstance(data, dict) and 'graphs' in data:
        data = data['graphs']
    # Case 4: Iterable of multiple graph objects and/or gJGF dicts (with single graph each)
    elif isinstance(data, _Iterable) and not isinstance(data, dict):
        try:
            num_items = len(data)
        except Exception:
            raise_error('Iterable without a fixed length.')
        if num_items == 0:
            raise_error('Iterable with zero items.')
        new_data = []
        for idx in range(num_items):
            item = data[idx]
            if is_known_graph_object(item):
                item = _convert.any_to_gjgf(item)
            elif isinstance(item, str):
                item = str_to_json_object(item)
            elif isinstance(item, dict) and 'graph' in item:
                pass
            else:
                raise_error('Iterable with invalid item at position {}.'.format(idx))
            new_data.append(item['graph'])
        data = new_data
    # Case 5: Other unknown data
    else:
        raise_error()
    return data


def is_known_graph_object(data):
    """Check if the given data is a graph object from one of the supported libraries."""
    result = False
    try:
        dtype = str(type(data)).lower()
        if isinstance(data, list):
            dtype_inner = str(type(data[0])).lower()
            if 'networkit' in dtype_inner:
                dtype = dtype_inner
        result = ('graph_tool.graph' in dtype) or \
            ('igraph.graph' in dtype) or \
            ('networkit' in dtype) or \
            ('networkx.classes' in dtype) or \
            ('snap' in dtype)
    except Exception:
        pass
    return result


def prepare_gjgf_dict():
    """Create the basic structure for a nested dictionary adhering to gJGF."""
    data = {'graph': {'nodes': {}, 'edges': []}}
    data_graph = data['graph']
    data_nodes = data['graph']['nodes']
    data_edges = data['graph']['edges']
    return data, data_graph, data_nodes, data_edges


def insert_graph_data(data_graph, graph_directed, graph_metadata_dict):
    """Insert graph data into a nested dictionary adhering to gJGF in the right levels."""
    data_graph['directed'] = graph_directed
    if isinstance(graph_metadata_dict, dict) and graph_metadata_dict:
        # keys belonging to data level
        for key in ('label', 'type'):
            if key in graph_metadata_dict:
                data_graph[key] = graph_metadata_dict.pop(key)
        # keys belonging to metadata level
        if graph_metadata_dict:
            data_graph['metadata'] = graph_metadata_dict


def insert_node_data(data_nodes, node_id, node_metadata_dict):
    """Insert node data into a nested dictionary adhering to gJGF in the right levels."""
    node_dict = {}
    if isinstance(node_metadata_dict, dict) and node_metadata_dict:
        # keys belonging to data level
        for key in ('label', ):
            if key in node_metadata_dict:
                node_dict[key] = node_metadata_dict.pop(key)
        # keys belonging to metadata level
        if node_metadata_dict:
            node_dict['metadata'] = node_metadata_dict
    data_nodes[node_id] = node_dict


def insert_edge_data(data_edges, edge_source_id, edge_target_id, edge_metadata_dict):
    """Insert edge data into a nested dictionary adhering to gJGF in the right levels."""
    edge_dict = {
        'source': edge_source_id,
        'target': edge_target_id,
    }
    if isinstance(edge_metadata_dict, dict) and edge_metadata_dict:
        # keys belonging to data level
        for key in ('id', 'label', 'relation', 'directed'):
            if key in edge_metadata_dict:
                edge_dict[key] = edge_metadata_dict.pop(key)
        # keys belonging to metadata level
        if edge_metadata_dict:
            edge_dict['metadata'] = edge_metadata_dict
    data_edges.append(edge_dict)
