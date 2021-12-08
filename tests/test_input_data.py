import os

import pytest
import shared

import gravis as gv


def test_input_single_gjgf(my_outdir):
    single_gjgf_string = """{
        "graph": {
            "label": "gJGF example",
            "nodes": [{"id": 0}, {"id": 1}],
            "edges": [{"source": 0, "target": 1}, {"source": 0, "target": 1}]
        }
    }"""
    single_gjgf_object = {
        'graph': {
            'label': 'gJGF example',
            'nodes': [{'id': 0}, {'id': 1}],
            'edges': [{'source': 0, 'target': 1}, {'source': 0, 'target': 1}],
        }
    }

    data = single_gjgf_string
    fig = gv.d3(data)
    filepath = os.path.join(my_outdir, 'single_gjgf_str_d3')
    shared.export_all_available_formats(fig, filepath)

    data = single_gjgf_object
    fig = gv.d3(data)
    filepath = os.path.join(my_outdir, 'single_gjgf_obj_d3')
    shared.export_all_available_formats(fig, filepath)

    fig = gv.vis(data)
    filepath = os.path.join(my_outdir, 'single_gjgf_vis')
    shared.export_all_available_formats(fig, filepath)

    fig = gv.three(data)
    filepath = os.path.join(my_outdir, 'single_gjgf_three')
    shared.export_all_available_formats(fig, filepath)


def test_input_single_gjgf_from_file(my_outdir):
    data = os.path.join(shared.IN_DIR, 'gjgf_graph_single.json')
    fig = gv.d3(data)
    filepath = os.path.join(my_outdir, 'single_gjgf_file_d3')
    shared.export_all_available_formats(fig, filepath)

    fig = gv.vis(data)
    filepath = os.path.join(my_outdir, 'single_gjgf_file_vis')
    shared.export_all_available_formats(fig, filepath)

    fig = gv.three(data)
    filepath = os.path.join(my_outdir, 'single_gjgf_file_three')
    shared.export_all_available_formats(fig, filepath)


def test_input_single_graph(my_outdir):
    data = shared.TESTDATA_NETWORKX['undirected']
    fig = gv.d3(data)
    filepath = os.path.join(my_outdir, 'single_nx_graph_d3')
    shared.export_all_available_formats(fig, filepath)

    fig = gv.vis(data)
    filepath = os.path.join(my_outdir, 'single_nx_graph_vis')
    shared.export_all_available_formats(fig, filepath)

    fig = gv.three(data)
    filepath = os.path.join(my_outdir, 'single_nx_graph_three')
    shared.export_all_available_formats(fig, filepath)


def test_input_multiple_gjgf(my_outdir):
    multiple_gjgf = {
        'graphs': [
            {
                'nodes': [{'id': 0}, {'id': 1}],
                'edges': [{'source': 0, 'target': 1}, {'source': 0, 'target': 1}],
            },
            {
                'nodes': [{'id': 0}, {'id': 1}, {'id': 2}],
                'edges': [{'source': 0, 'target': 1}, {'source': 0, 'target': 2}],
            },
            '{"graph": {"label": "gJGF example","nodes": [{"id": 0}, {"id": 1}],"edges": [{"source": 0, "target": 1}, {"source": 0, "target": 1}]}}',
            {
                'nodes': [{'id': 0}, {'id': 1}, {'id': 2}, {'id': 3}],
                'edges': [{'source': 0, 'target': 1}, {'source': 0, 'target': 3}],
            },
            """{
        "graph": {
            "label": "gJGF example",
            "nodes": [{"id": 0}, {"id": 1}],
            "edges": [{"source": 0, "target": 1}, {"source": 0, "target": 1}]
        }
    }"""
        ]
    }
    data = multiple_gjgf
    fig = gv.d3(data)
    filepath = os.path.join(my_outdir, 'multiple_gjgf_d3')
    shared.export_all_available_formats(fig, filepath)

    fig = gv.vis(data)
    filepath = os.path.join(my_outdir, 'multiple_gjgf_vis')
    shared.export_all_available_formats(fig, filepath)

    fig = gv.three(data)
    filepath = os.path.join(my_outdir, 'multiple_gjgf_three')
    shared.export_all_available_formats(fig, filepath)


def test_input_multiple_gjgf_from_file(my_outdir):
    data = os.path.join(shared.IN_DIR, 'gjgf_graph_multiple.json')

    fig = gv.d3(data)
    filepath = os.path.join(my_outdir, 'multiple_gjgf_file_d3')
    shared.export_all_available_formats(fig, filepath)

    fig = gv.vis(data)
    filepath = os.path.join(my_outdir, 'multiple_gjgf_file_vis')
    shared.export_all_available_formats(fig, filepath)

    fig = gv.three(data)
    filepath = os.path.join(my_outdir, 'multiple_gjgf_file_three')
    shared.export_all_available_formats(fig, filepath)


@pytest.mark.only_with_graph_libraries
def test_input_multiple_graph_and_gjgf(my_outdir):
    gjgf_graph_empty = {
        'graph': {
            'label': 'Empty gJGF',
            'nodes': [],
            'edges': [],
        }
    }
    gjgf_graph_one_node = {
        'graph': {
            'label': 'gJGF with 1 node',
            'nodes': [{'id': 0}],
            'edges': [],
        }
    }
    gjgf_graph_two_nodes = {
        'graph': {
            'label': 'gJGF with 2 nodes',
            'nodes': [{'id': 0}, {'id': 1}],
            'edges': [],
        }
    }
    gjgf_graph_two_nodes_and_multiedge = {
        'graph': {
            'label': 'gJGF with 2 nodes and 2 undirected edges (multiedge)',
            'nodes': [{'id': 0}, {'id': 1}],
            'edges': [{'source': 0, 'target': 1}, {'source': 0, 'target': 1}],
        }
    }
    data = [
        gjgf_graph_empty,
        gjgf_graph_one_node,
        gjgf_graph_two_nodes,
        gjgf_graph_two_nodes_and_multiedge,
        shared.TESTDATA_GJGF['undirected attributed'],
        shared.TESTDATA_GJGF['directed attributed'],
        shared.TESTDATA_GRAPH_TOOL['undirected attributed'],
        shared.TESTDATA_GRAPH_TOOL['directed attributed'],
        shared.TESTDATA_IGRAPH['undirected attributed'],
        shared.TESTDATA_IGRAPH['directed attributed'],
        shared.TESTDATA_NETWORKIT['undirected'],
        shared.TESTDATA_NETWORKIT['directed'],
        shared.TESTDATA_NETWORKX['undirected attributed'],
        shared.TESTDATA_NETWORKX['directed attributed'],
        shared.TESTDATA_PYNTACLE['undirected attributed'],
        shared.TESTDATA_PYNTACLE['directed attributed'],
        shared.TESTDATA_SNAP['undirected'],
        shared.TESTDATA_SNAP['directed'],
    ]
    fig = gv.d3(data)
    filepath = os.path.join(my_outdir, 'multiple_graph_and_gjgf_d3')
    shared.export_all_available_formats(fig, filepath)

    fig = gv.vis(data)
    filepath = os.path.join(my_outdir, 'multiple_graph_and_gjgf_vis')
    shared.export_all_available_formats(fig, filepath)

    fig = gv.three(data)
    filepath = os.path.join(my_outdir, 'multiple_graph_and_gjgf_three')
    shared.export_all_available_formats(fig, filepath)


def test_input_larger_gjgf(my_outdir):
    data = {
        'graph': {
            'directed': True,
            'metadata': {
                'arrow_size': 5,
                'background_color': 'black',
                'edge_size': 3,
                'edge_label_size': 14,
                'edge_label_color': 'white',
                'node_size': 15,
                'node_color': 'white',
            },
            'nodes': [
                {'id': 1, 'metadata': {'shape': 'rectangle', 'y': 200, 'label': 'node_label'}},
                {'id': 2},
                {'id': 3},
                {'id': 4, 'metadata': {'shape': 'rectangle', 'y': 200}},
                {'id': 5, 'metadata': {'shape': 'hexagon', 'y': 0}},
            ],
            'edges': [
                {'source': 1, 'target': 2, 'metadata': {
                    'color': '#d73027', 'de': 'Das',   'en': 'This', 'label': 'edge_label'}},
                {'source': 2, 'target': 3, 'metadata': {
                    'color': '#f46d43', 'de': 'ist',   'en': 'is'}},
                {'source': 3, 'target': 1, 'metadata': {
                    'color': '#fdae61', 'de': 'das',   'en': 'the'}},
                {'source': 1, 'target': 4, 'metadata': {
                    'color': '#fee08b', 'de': 'Haus',  'en': 'house'}},
                {'source': 4, 'target': 3, 'metadata': {
                    'color': '#d9ef8b', 'de': 'vom',   'en': 'of'}},
                {'source': 3, 'target': 5, 'metadata': {
                    'color': '#a6d96a', 'de': 'Ni-.',  'en': 'San-'}},
                {'source': 5, 'target': 2, 'metadata': {
                    'color': '#66bd63', 'de': 'ko-',   'en': 'ta'}},
                {'source': 2, 'target': 4, 'metadata': {
                    'color': '#1a9850', 'de': 'laus.', 'en': 'Claus.'}},
            ],
        }
    }

    fig = gv.d3(data)
    filepath = os.path.join(my_outdir, 'larger_gjgf_d3')
    shared.export_all_available_formats(fig, filepath)


@pytest.mark.only_with_graph_libraries
def test_input_larger_graph(my_outdir):
    data = shared.TESTDATA_NETWORKX['directed attributed 2']
    fig = gv.d3(data)
    filepath = os.path.join(my_outdir, 'larger_networkx_d3')
    shared.export_all_available_formats(fig, filepath)


def test_input_fail_on_invalid_data():
    def d3_fails(data):
        with pytest.raises(ValueError):
            gv.d3(data)

    def vis_fails(data):
        with pytest.raises(ValueError):
            gv.vis(data)

    def three_fails(data):
        with pytest.raises(ValueError):
            gv.three(data)

    gjgf_graph = {
        'graph': {
            'nodes': [{'id': 0}],
            'edges': [],
        }
    }

    generator = (x for x in range(5))
    for nonsense_item in [1, 'a', None, [], generator, [1], ['a'], {}, {'a': 1}, {1: 'a'}]:
        data = nonsense_item
        d3_fails(data)
        vis_fails(data)
        three_fails(data)

        data = [nonsense_item, nonsense_item, nonsense_item]
        d3_fails(data)
        vis_fails(data)
        three_fails(data)

        data = [gjgf_graph, nonsense_item]
        d3_fails(data)
        vis_fails(data)
        three_fails(data)

        data = [nonsense_item, gjgf_graph]
        d3_fails(data)
        vis_fails(data)
        three_fails(data)


def test_fail_on_invalid_graph_object():
    class NonsenseGraph:
        pass

    data = NonsenseGraph()
    with pytest.raises(ValueError):
        gv.d3(data)
    with pytest.raises(ValueError):
        gv.convert.any_to_gjgf(data)


def test_os(tmpdir):
    is_file = gv._internal.utils.operating_system.is_file
    is_nonempty_file = gv._internal.utils.operating_system.is_nonempty_file

    with tmpdir.as_cwd():
        filepath = 'test1.txt'
        # File does not exist
        assert not is_file(filepath)
        assert not is_nonempty_file(filepath)
        # File exists
        with open(filepath, 'w') as f:
            f.write('hello, world!')
        assert is_file(filepath)
        assert is_nonempty_file(filepath)
        with pytest.raises(FileExistsError):
            is_file(filepath, raise_exception=True)
        with pytest.raises(FileExistsError):
            is_nonempty_file(filepath, raise_exception=True)
