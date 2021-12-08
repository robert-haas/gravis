import os

import pytest
import shared

import gravis as gv


@pytest.mark.only_with_graph_libraries
def test_graph_library_conversion_and_result_equivalence(my_outdir):
    if shared.TESTDATA_GRAPH_TOOL is None:
        raise ValueError('Data generation with graph-tool failed. Is the package installed?')
    if shared.TESTDATA_IGRAPH is None:
        raise ValueError('Data generation with igraph failed. Is the package installed?')
    if shared.TESTDATA_NETWORKIT is None:  # no attributes
        raise ValueError('Data generation with NetworKit failed. Is the package installed?')
    if shared.TESTDATA_NETWORKX is None:
        raise ValueError('Data generation with NetworkX failed. Is the package installed?')
    if shared.TESTDATA_PYNTACLE is None:  # igraph
        raise ValueError('Data generation with Pyntacle failed. Is the package installed?')
    if shared.TESTDATA_SNAP is None:  # only directed can have attributes, no graph attributes
        raise ValueError('Data generation with SNAP failed. Is the package installed?')

    # undirected graphs
    gjgf_gt = gv.convert.graphtool_to_gjgf(shared.TESTDATA_GRAPH_TOOL['undirected'])
    gjgf_ig = gv.convert.igraph_to_gjgf(shared.TESTDATA_IGRAPH['undirected'])
    gjgf_nk = gv.convert.networkit_to_gjgf(shared.TESTDATA_NETWORKIT['undirected'])
    gjgf_nx = gv.convert.networkx_to_gjgf(shared.TESTDATA_NETWORKX['undirected'])
    gjgf_pn = gv.convert.pyntacle_to_gjgf(shared.TESTDATA_PYNTACLE['undirected'])
    gjgf_sn = gv.convert.snap_to_gjgf(shared.TESTDATA_SNAP['undirected'])

    assert gjgf_gt == gv.convert.any_to_gjgf(shared.TESTDATA_GRAPH_TOOL['undirected'])
    assert gjgf_ig == gv.convert.any_to_gjgf(shared.TESTDATA_IGRAPH['undirected'])
    assert gjgf_nk == gv.convert.any_to_gjgf(shared.TESTDATA_NETWORKIT['undirected'])
    assert gjgf_nx == gv.convert.any_to_gjgf(shared.TESTDATA_NETWORKX['undirected'])
    assert gjgf_pn == gv.convert.any_to_gjgf(shared.TESTDATA_PYNTACLE['undirected'])
    assert gjgf_sn == gv.convert.any_to_gjgf(shared.TESTDATA_SNAP['undirected'])

    fig = gv.d3(gjgf_gt)
    filepath = os.path.join(my_outdir, 'graphtool_d3_undirected')
    shared.export_all_available_formats(fig, filepath)

    fig = gv.d3(gjgf_ig)
    filepath = os.path.join(my_outdir, 'igraph_d3_undirected')
    shared.export_all_available_formats(fig, filepath)

    fig = gv.d3(gjgf_nk)
    filepath = os.path.join(my_outdir, 'networkit_d3_undirected')
    shared.export_all_available_formats(fig, filepath)

    fig = gv.d3(gjgf_nx)
    filepath = os.path.join(my_outdir, 'networkx_d3_undirected')
    shared.export_all_available_formats(fig, filepath)

    fig = gv.d3(gjgf_pn)
    filepath = os.path.join(my_outdir, 'pyntacle_d3_undirected')
    shared.export_all_available_formats(fig, filepath)

    fig = gv.d3(gjgf_sn)
    filepath = os.path.join(my_outdir, 'snap_d3_undirected')
    shared.export_all_available_formats(fig, filepath)

    # directed graphs
    gjgf_gt = gv.convert.graphtool_to_gjgf(shared.TESTDATA_GRAPH_TOOL['directed'])
    gjgf_ig = gv.convert.igraph_to_gjgf(shared.TESTDATA_IGRAPH['directed'])
    gjgf_nk = gv.convert.networkit_to_gjgf(shared.TESTDATA_NETWORKIT['directed'])
    gjgf_nx = gv.convert.networkx_to_gjgf(shared.TESTDATA_NETWORKX['directed'])
    gjgf_pn = gv.convert.pyntacle_to_gjgf(shared.TESTDATA_PYNTACLE['directed'])
    gjgf_sn = gv.convert.snap_to_gjgf(shared.TESTDATA_SNAP['directed'])
    assert gjgf_gt == gjgf_ig == gjgf_nk == gjgf_nx == gjgf_pn == gjgf_sn

    assert gjgf_gt == gv.convert.any_to_gjgf(shared.TESTDATA_GRAPH_TOOL['directed'])
    assert gjgf_ig == gv.convert.any_to_gjgf(shared.TESTDATA_IGRAPH['directed'])
    assert gjgf_nk == gv.convert.any_to_gjgf(shared.TESTDATA_NETWORKIT['directed'])
    assert gjgf_nx == gv.convert.any_to_gjgf(shared.TESTDATA_NETWORKX['directed'])
    assert gjgf_pn == gv.convert.any_to_gjgf(shared.TESTDATA_PYNTACLE['directed'])
    assert gjgf_sn == gv.convert.any_to_gjgf(shared.TESTDATA_SNAP['directed'])

    fig = gv.d3(gjgf_gt)
    filepath = os.path.join(my_outdir, 'graphtool_d3_directed')
    shared.export_all_available_formats(fig, filepath)

    fig = gv.d3(gjgf_ig)
    filepath = os.path.join(my_outdir, 'igraph_d3_directed')
    shared.export_all_available_formats(fig, filepath)

    fig = gv.d3(gjgf_nk)
    filepath = os.path.join(my_outdir, 'networkit_d3_directed')
    shared.export_all_available_formats(fig, filepath)

    fig = gv.d3(gjgf_nx)
    filepath = os.path.join(my_outdir, 'networkx_d3_directed')
    shared.export_all_available_formats(fig, filepath)

    fig = gv.d3(gjgf_pn)
    filepath = os.path.join(my_outdir, 'pyntacle_d3_directed')
    shared.export_all_available_formats(fig, filepath)

    fig = gv.d3(gjgf_sn)
    filepath = os.path.join(my_outdir, 'snap_d3_directed')
    shared.export_all_available_formats(fig, filepath)

    # undirected graphs with attributes
    gjgf_gt = gv.convert.graphtool_to_gjgf(shared.TESTDATA_GRAPH_TOOL['undirected attributed'])
    gjgf_ig = gv.convert.igraph_to_gjgf(shared.TESTDATA_IGRAPH['undirected attributed'])
    gjgf_nx = gv.convert.networkx_to_gjgf(shared.TESTDATA_NETWORKX['undirected attributed'])
    gjgf_pn = gv.convert.pyntacle_to_gjgf(shared.TESTDATA_PYNTACLE['undirected attributed'])
    # assert gjgf_gt == gjgf_ig == gjgf_nx == gjgf_pn  # source/target arbitrary

    assert gjgf_gt == gv.convert.any_to_gjgf(shared.TESTDATA_GRAPH_TOOL['undirected attributed'])
    assert gjgf_ig == gv.convert.any_to_gjgf(shared.TESTDATA_IGRAPH['undirected attributed'])
    assert gjgf_nx == gv.convert.any_to_gjgf(shared.TESTDATA_NETWORKX['undirected attributed'])
    assert gjgf_pn == gv.convert.any_to_gjgf(shared.TESTDATA_PYNTACLE['undirected attributed'])

    fig = gv.d3(gjgf_gt)
    filepath = os.path.join(my_outdir, 'graphtool_d3_undirected_attributed')
    shared.export_all_available_formats(fig, filepath)

    fig = gv.d3(gjgf_ig)
    filepath = os.path.join(my_outdir, 'igraph_d3_undirected_attributed')
    shared.export_all_available_formats(fig, filepath)

    fig = gv.d3(gjgf_nx)
    filepath = os.path.join(my_outdir, 'networkx_d3_undirected_attributed')
    shared.export_all_available_formats(fig, filepath)

    fig = gv.d3(gjgf_pn)
    filepath = os.path.join(my_outdir, 'pyntacle_d3_undirected_attributed')
    shared.export_all_available_formats(fig, filepath)

    # directed graphs with attributes
    gjgf_gt = gv.convert.graphtool_to_gjgf(shared.TESTDATA_GRAPH_TOOL['directed attributed'])
    gjgf_ig = gv.convert.igraph_to_gjgf(shared.TESTDATA_IGRAPH['directed attributed'])
    gjgf_nx = gv.convert.networkx_to_gjgf(shared.TESTDATA_NETWORKX['directed attributed'])
    gjgf_pn = gv.convert.pyntacle_to_gjgf(shared.TESTDATA_PYNTACLE['directed attributed'])
    gjgf_sn = gv.convert.snap_to_gjgf(shared.TESTDATA_SNAP['directed attributed'])
    assert gjgf_gt == gjgf_ig == gjgf_nx == gjgf_pn  # gjgf_sn does not have graph properties

    assert gjgf_gt == gv.convert.any_to_gjgf(shared.TESTDATA_GRAPH_TOOL['directed attributed'])
    assert gjgf_ig == gv.convert.any_to_gjgf(shared.TESTDATA_IGRAPH['directed attributed'])
    assert gjgf_nx == gv.convert.any_to_gjgf(shared.TESTDATA_NETWORKX['directed attributed'])
    assert gjgf_pn == gv.convert.any_to_gjgf(shared.TESTDATA_PYNTACLE['directed attributed'])
    assert gjgf_sn == gv.convert.any_to_gjgf(shared.TESTDATA_SNAP['directed attributed'])

    fig = gv.d3(gjgf_gt)
    filepath = os.path.join(my_outdir, 'graphtool_d3_directed_attributed')
    shared.export_all_available_formats(fig, filepath)

    fig = gv.d3(gjgf_ig)
    filepath = os.path.join(my_outdir, 'igraph_d3_directed_attributed')
    shared.export_all_available_formats(fig, filepath)

    fig = gv.d3(gjgf_nx)
    filepath = os.path.join(my_outdir, 'networkx_d3_directed_attributed')
    shared.export_all_available_formats(fig, filepath)

    fig = gv.d3(gjgf_pn)
    filepath = os.path.join(my_outdir, 'pyntacle_d3_directed_attributed')
    shared.export_all_available_formats(fig, filepath)

    fig = gv.d3(gjgf_sn)
    filepath = os.path.join(my_outdir, 'snap_d3_directed_attributed')
    shared.export_all_available_formats(fig, filepath)


@pytest.mark.only_with_graph_libraries
def test_graph_library_conversion_with_multiple_graphs():
    graphs = [
        shared.TESTDATA_GRAPH_TOOL['undirected'],
        shared.TESTDATA_IGRAPH['undirected'],
        shared.TESTDATA_NETWORKIT['undirected'],
        shared.TESTDATA_NETWORKX['undirected'],
        shared.TESTDATA_PYNTACLE['undirected'],
        shared.TESTDATA_SNAP['undirected'],

        shared.TESTDATA_GRAPH_TOOL['directed'],
        shared.TESTDATA_IGRAPH['directed'],
        shared.TESTDATA_NETWORKIT['directed'],
        shared.TESTDATA_NETWORKX['directed'],
        shared.TESTDATA_PYNTACLE['directed'],
        shared.TESTDATA_SNAP['directed'],

        shared.TESTDATA_GRAPH_TOOL['undirected attributed'],
        shared.TESTDATA_IGRAPH['undirected attributed'],
        shared.TESTDATA_NETWORKX['undirected attributed'],
        shared.TESTDATA_PYNTACLE['undirected attributed'],

        shared.TESTDATA_GRAPH_TOOL['directed attributed'],
        shared.TESTDATA_IGRAPH['directed attributed'],
        shared.TESTDATA_NETWORKX['directed attributed'],
        shared.TESTDATA_PYNTACLE['directed attributed'],
        shared.TESTDATA_SNAP['directed attributed'],
    ]
    gjgf = gv.convert.multiple_to_gjgf(graphs)
    assert isinstance(gjgf, dict)
    assert isinstance(gjgf['graphs'], list)
    for graph in gjgf['graphs']:
        assert isinstance(graph, dict)
        assert 'nodes' in graph
        assert 'edges' in graph

    assert len(gv.d3(graphs).to_html()) == len(gv.d3(gjgf).to_html())
    assert len(gv.vis(graphs).to_html()) == len(gv.vis(gjgf).to_html())
    assert len(gv.three(graphs).to_html()) == len(gv.three(gjgf).to_html())

    # One invalid graph
    with pytest.raises(ValueError):
        graphs[4] = 'nonsense'
        gv.convert.multiple_to_gjgf(graphs)


@pytest.mark.only_with_graph_libraries
def test_graph_library_networkit_with_metadata_via_list_with_dicts(my_outdir):
    if shared.TESTDATA_NETWORKIT is None:  # no attributes
        raise ValueError('Data generation with NetworKit failed. Is the package installed?')

    graph = shared.TESTDATA_NETWORKIT['undirected']
    graph_metadata = {'background_color': 'gray', 'node_color': 'red', 'edge_color': 'blue'}

    node_metadata = {}

    def parse_node(node):
        node_metadata[node] = {'size': 50, 'opacity': 0.5}
    graph.forNodes(parse_node)

    edge_metadata = {}

    def parse_edge(s, t, ea, eb):
        edge_metadata['({}, {})'.format(s, t)] = {'size': 10}
    graph.forEdges(parse_edge)

    d0 = graph
    d1 = [graph, graph_metadata]
    d2 = [graph, graph_metadata, node_metadata]
    d3 = [graph, graph_metadata, node_metadata, edge_metadata]
    d4 = [graph, graph_metadata, [], []]  # just to cover edge cases in code

    for i, data in enumerate([d0, d1, d2, d3, d4]):
        fig = gv.d3(data)
        filepath = os.path.join(my_outdir, 'networkit_d3_metadata_{}'.format(i))
        shared.export_all_available_formats(fig, filepath)
