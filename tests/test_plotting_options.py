import os
from copy import deepcopy

import pytest
import shared

import gravis as gv


def test_plotting_fig(my_outdir):
    data = shared.TESTDATA_NETWORKX['undirected']
    for func in [gv.d3, gv.vis, gv.three]:
        # Figure creation
        fig = func(data, show_edge_label=True)

        # Text representations
        strings = [
            repr(fig),
            str(fig),
            fig._repr_html_(),
            fig.to_html(),
            fig.to_html_standalone(),
            fig.to_html_partial(),
        ]
        for s in strings:
            assert isinstance(s, str)
            assert len(s) > 20

        # Display variants
        fig.display()
        fig.display(inline=True)

        # Export
        filepath = os.path.join(my_outdir, 'an_overwritten_file.html')
        fig.export_html(filepath, overwrite=True)
        with pytest.raises(FileExistsError):
            fig.export_html(filepath, overwrite=False)


@pytest.mark.only_with_graph_libraries
def test_plotting_fig_and_exporting_static_image(my_outdir):
    data = shared.TESTDATA_NETWORKX['undirected']

    for driver in ('firefox', 'chrome'):
        # d3
        fig = gv.d3(data)

        filepath = os.path.join(my_outdir, 'd3_{}.png'.format(driver))
        fig.export_png(filepath, webdriver=driver, capture_delay=0.5, overwrite=True)
        with pytest.raises(FileExistsError):
            fig.export_png(filepath)

        filepath = os.path.join(my_outdir, 'd3_{}.jpg'.format(driver))
        fig.export_jpg(filepath, webdriver=driver, capture_delay=0.5, overwrite=True)
        with pytest.raises(FileExistsError):
            fig.export_jpg(filepath)

        filepath = os.path.join(my_outdir, 'd3_{}.svg'.format(driver))
        fig.export_svg(filepath, webdriver=driver, capture_delay=0.5, overwrite=True)
        with pytest.raises(FileExistsError):
            fig.export_svg(filepath)

        # vis
        fig = gv.vis(data)
        filepath = os.path.join(my_outdir, 'vis_{}.png'.format(driver))
        fig.export_png(filepath, webdriver=driver, capture_delay=0.5, overwrite=True)
        with pytest.raises(FileExistsError):
            fig.export_png(filepath)

        filepath = os.path.join(my_outdir, 'vis_{}.jpg'.format(driver))
        fig.export_jpg(filepath, webdriver=driver, capture_delay=0.5, overwrite=True)
        with pytest.raises(FileExistsError):
            fig.export_jpg(filepath)

        filepath = os.path.join(my_outdir, 'vis_{}.svg'.format(driver))
        with pytest.raises(ValueError):
            fig.export_svg(filepath, webdriver=driver, capture_delay=0.5, overwrite=True)

        # three
        fig = gv.three(data)
        filepath = os.path.join(my_outdir, 'three_{}.png'.format(driver))
        fig.export_png(filepath, webdriver=driver, capture_delay=1.5, overwrite=True)
        with pytest.raises(FileExistsError):
            fig.export_png(filepath)

        filepath = os.path.join(my_outdir, 'three_{}.jpg'.format(driver))
        fig.export_jpg(filepath, webdriver=driver, capture_delay=1.5, overwrite=True)
        with pytest.raises(FileExistsError):
            fig.export_jpg(filepath)

        filepath = os.path.join(my_outdir, 'three_{}.svg'.format(driver))
        with pytest.raises(ValueError):
            fig.export_svg(filepath, webdriver=driver, capture_delay=1.5, overwrite=True)


def test_plotting_with_each_keyword_argument(my_outdir):
    # Note: All outputs were inspected manually, all bugs were resolved and all shortcomings
    # documented in the docstrings. This becomes necessary again in case of major code changes
    # and can hardly be automated (with reasonable effort).
    data_undirected = {
        "graph": {
            "label": "a graph",
            "metadata": {
                "arrow_color": "green",
                "arrow_size": 10,
                "background_color": "#ffe",
                "node_shape": "hexagon",
                "node_size": 60,
                "node_color": "gray",
                "node_opacity": 1.0,
                "node_hover": "hovered node",
                "node_click": "clicked node",
                "edge_size": 1,
                "edge_color": "magenta",
                "edge_opacity": 1.0,
                "edge_hover": "hovered edge",
                "edge_click": "clicked edge",
            },
            "nodes": [
                {"id": 1, "label": "node a", "metadata": {"size": 20, "shape": "circle"}},
                {"id": 2, "label": "node b", "metadata": {"size": 30, "shape": "rectangle",
                 "color": "red", "opacity": 0.5, "x": -100.0, "y": 10.0}},
                {"id": 3},
                {"id": 4, "label": "node d", "metadata": {"size": 5,
                 "color": "green", "opacity": 0.25, "x": 100.0, "y": 80.0}},
                {"id": 5, "label": "node e", "metadata": {"shape": "hexagon",
                 "color": "blue", "opacity": 0.1, "x": 50.0, "y": 80.0}},
                {"id": 6, "metadata": {"image": gv.convert.image_to_data_url(
                    os.path.join(shared.IN_DIR, 'rectangle_30x10.png'))}},
                {"id": 7, "metadata": {"image": gv.convert.image_to_data_url(
                    os.path.join(shared.IN_DIR, 'rectangle_10x10.png'))}},
            ],
            "edges": [
                {"source": 1, "target": 2},
                {"source": 1, "target": 2, "metadata": {"size": 1, "color": "black"}},
                {"source": 1, "target": 2, "metadata": {"size": 1, "color": "gray"}},
                {"source": 2, "target": 3},
                {"source": 3, "target": 4},
                {"source": 3, "target": 3, "metadata": {"color": "blue"}},
                {"source": 3, "target": 3,
                 "metadata": {"color": "orange", "size": 3, "opacity": 0.2}},
                {"source": 4, "target": 1, "metadata": {"opacity": 0.5}},
                {"source": 1, "target": 5},
                {"source": 2, "target": 6},
                {"source": 6, "target": 7},
            ]
        }
    }
    data_directed = deepcopy(data_undirected)
    data_directed['graph']['directed'] = True

    def create_d3_plot(directed, key, val):
        base_name = 'kwarg_{}_{}_{}_{}'
        fig = gv.d3(data, **{key: val})
        filename = base_name.format(str(key), str(val), directed, 'd3')
        filepath = os.path.join(my_outdir, filename)
        shared.export_all_available_formats(fig, filepath)

    def create_three_plot(directed, key, val):
        base_name = 'kwarg_{}_{}_{}_{}'
        fig = gv.three(data, **{key: val})
        filename = base_name.format(str(key), str(val), directed, 'three')
        filepath = os.path.join(my_outdir, filename)
        shared.export_all_available_formats(fig, filepath)

    def create_vis_plot(directed, key, val):
        base_name = 'kwarg_{}_{}_{}_{}'
        fig = gv.vis(data, **{key: val})
        filename = base_name.format(str(key), str(val), directed, 'vis')
        filepath = os.path.join(my_outdir, filename)
        shared.export_all_available_formats(fig, filepath)

    kwargs_all = dict(
        graph_height=40,
        details_height=40,
        show_details=True,
        show_menu=False,
        show_node=False,
        node_size_factor=2.0,
        node_size_data_source='label_size',
        use_node_size_normalization=True,
        node_size_normalization_min=1.0,
        node_size_normalization_max=200.0,
        node_drag_fix=True,
        node_hover_neighborhood=True,
        node_hover_tooltip=False,
        show_node_image=False,
        node_image_size_factor=2.0,
        show_node_label=False,
        show_node_label_border=False,
        node_label_data_source='size',
        node_label_size_factor=2.0,
        node_label_rotation=30,
        node_label_font='mono',
        show_edge=False,
        edge_size_factor=5.0,
        edge_size_data_source='label_size',
        use_edge_size_normalization=True,
        edge_size_normalization_min=2.0,
        edge_size_normalization_max=20.0,
        edge_curvature=-1.2,
        edge_hover_tooltip=False,
        show_edge_label=True,
        show_edge_label_border=False,
        edge_label_data_source='size',
        edge_label_size_factor=5.0,
        edge_label_rotation=30.0,
        edge_label_font='mono',
        zoom_factor=3.0,
        large_graph_threshold=2,
        layout_algorithm_active=False,
    )

    kwargs_d3_specific = dict(
        use_many_body_force=False,
        many_body_force_strength=-500.0,
        many_body_force_theta=0.01,
        use_many_body_force_min_distance=True,
        many_body_force_min_distance=1000.0,
        use_many_body_force_max_distance=True,
        many_body_force_max_distance=10.0,
        use_links_force=False,
        links_force_distance=500.0,
        links_force_strength=1.0,
        use_collision_force=True,
        collision_force_radius=10.0,
        collision_force_strength=0.01,
        use_x_positioning_force=True,
        x_positioning_force_strength=1.0,
        use_y_positioning_force=True,
        y_positioning_force_strength=1.0,
        use_centering_force=False,
    )

    kwargs_three_specific = dict(
        use_many_body_force=False,
        many_body_force_strength=-500.0,
        many_body_force_theta=0.01,
        use_many_body_force_min_distance=True,
        many_body_force_min_distance=1000.0,
        use_many_body_force_max_distance=True,
        many_body_force_max_distance=10.0,
        use_links_force=False,
        links_force_distance=500.0,
        links_force_strength=1.0,
        use_x_positioning_force=True,
        x_positioning_force_strength=1.0,
        use_y_positioning_force=True,
        y_positioning_force_strength=1.0,
        use_centering_force=False,
        z_positioning_force_strength=1.0,
        use_z_positioning_force=True,
    )

    kwargs_vis_specific = dict(
        layout_algorithm='forceAtlas2Based',
        gravitational_constant=-100000.0,
        central_gravity=10.0,
        spring_length=300.0,
        spring_constant=0.2,
        avoid_overlap=0.0
    )

    for directed, data in zip(['directed', 'undirected'], [data_directed, data_undirected]):
        for key, val in kwargs_all.items():
            create_d3_plot(directed, key, val)
            create_three_plot(directed, key, val)
            create_vis_plot(directed, key, val)
        for key, val in kwargs_d3_specific.items():
            create_d3_plot(directed, key, val)
        for key, val in kwargs_three_specific.items():
            create_three_plot(directed, key, val)
        for key, val in kwargs_vis_specific.items():
            create_vis_plot(directed, key, val)


def test_plotting_with_each_graph_data_property(my_outdir):
    # Note: All outputs were inspected manually, all bugs were resolved and all shortcomings
    # documented in the docstrings and below here. This becomes necessary again in case of
    # major code changes and can hardly be automated (with reasonable effort).
    """
1. **graph metadata**
  - arrow_color: d3, vis FAILS (not supported), three
  - arrow_size: d3, vis, three
  - background_color: d3, vis, three
  - node_color: d3, vis, three
  - node_opacity: d3, vis FAILS (not supported), three
  - node_size: d3, vis, three
  - node_shape: d3, vis (if no image), three
  - node_border_color: d3, vis, three FAILS (no border used)
  - node_border_size: d3, vis, three FAILS (no border used)
  - node_label_color: d3, vis, three
  - node_label_size: d3, vis, three
  - node_hover: d3, vis, three
  - node_click: d3, vis, three
  - node_image: d3, vis, three
  - node_x: d3, vis, three
  - node_y: d3, vis, three
  - node_z: three
  - edge_color: d3, vis, three
  - edge_opacity: d3, vis FAILS (not supported), three
  - edge_size: d3, vis, three
  - edge_label_color: d3, vis, three FAILS (no labels used)
  - edge_label_size: d3, vis, three FAILS (no labels used)
  - edge_hover: d3, vis, three
  - edge_click: d3, vis, three

2. **node metadata**
  - color: d3, vis, three
  - opacity: d3, vis FAILS (not supported), three
  - size: d3, vis, three
  - shape: d3, vis (if no image), three
  - border_color: d3, vis, three FAILS (no border used)
  - border_size: d3, vis, three FAILS (no border used)
  - label_color: d3, vis, three
  - label_size: d3, vis, three
  - hover: d3, vis, three
  - click: d3, vis, three
  - image: d3, vis, three
  - x: d3, vis, three
  - y: d3, vis, three
  - z: three

3. **edge metadata**
  - color: d3, vis, three
  - opacity: d3, vis FAILS (not supported), three
  - size: d3, vis, three
  - label_color: d3, vis, three FAILS (no labels)
  - label_size: d3, vis, three FAILS (no labels)
  - hover: d3, vis, three
  - click: d3, vis, three
"""

    plotting_functions = [
        ('d3', gv.d3),
        ('vis', gv.vis),
        ('three', gv.three),
    ]
    base_name = 'graph_arg_{}_{}'

    # all in one
    base_distance = 50.0
    data = {
        "graph": {
            "directed": True,
            "metadata": {
              "arrow_color": "yellow",
              "arrow_size": 30,
              "background_color": "lightgray",
              "node_color": "red",
              "node_opacity": 0.1,
              "node_size": 15,
              "node_shape": "hexagon",
              "node_border_color": "#fff",
              "node_border_size": 7,
              "node_label_color": "orange",
              "node_label_size": 5,
              "node_hover": "General node hover",
              "node_click": "General node click",
              "node_image": gv.convert.image_to_data_url(
                  os.path.join(shared.IN_DIR, 'rectangle_10x10.png')),
              "node_x": 0.0,
              "node_y": 0.0,
              "node_z": 0.0,
              "edge_color": "blue",
              "edge_opacity": 0.2,
              "edge_size": 4,
              "edge_label_color": "blue",
              "edge_label_size": 5,
              "edge_hover": "General edge hover",
              "edge_click": "General edge click",
            },
            "nodes": [
                {"id": 1, "label": "Node 1 special label", "metadata": {
                   "color": "#ff00ff",
                   "opacity": 0.75,
                   "size": 30,
                   "shape": "rectangle",
                   "border_color": "#aa00aa",
                   "border_size": 2,
                   "label_color": "#ff00ff",
                   "label_size": 30,
                   "hover": "Node $id special <span style='color:red'>hover</span> with HTML",
                   "click": "Node $id special <span style='color:orange'>click</span> with HTML",
                   "image": gv.convert.image_to_data_url(
                       os.path.join(shared.IN_DIR, 'rectangle_30x10.png')),
                   "x": base_distance,
                   "y": base_distance * 2,
                   "z": base_distance,
                }},
                {"id": 2, "label": "node b", "metadata": {
                  "shape": "circle",
                  "size": 40,
                  "image": gv.convert.image_to_data_url(
                      os.path.join(shared.IN_DIR, 'rectangle_30x10.png')),
                  "x": base_distance * 2,
                  "y": base_distance / 2,
                }},
                {"id": 3},
                {"id": 4, "label": "node d", "metadata": {
                  "size": 70,
                  "x": base_distance * 4,
                  "y": base_distance,
                }},
                {"id": 5, "label": "node e", "metadata": {
                  "shape": "hexagon",
                  "image": gv.convert.image_to_data_url(
                      os.path.join(shared.IN_DIR, 'rectangle_10x30.png')),
                  "x": base_distance * 5,
                  "y": base_distance * 3,
                }},
            ],
            "edges": [
                {"source": 1, "target": 2, "label": "Edge 1 special label", "metadata": {
                  "color": "#ff00ff",
                  "opacity": 0.75,
                  "size": 1,
                  "label_color": "#ff00ff",
                  "label_size": 30,
                  "hover": "Edge $id special <span style='color:blue'>hover</span> with HTML",
                  "click": "Edge $id special <span style='color:green'>click</span> with HTML",
                }},
                {"source": 2, "target": 3},
                {"source": 3, "target": 4},
                {"source": 4, "target": 1},
                {"source": 1, "target": 5},
            ]
        }
    }
    for func_name, func in plotting_functions:
        fig = func(data, show_edge_label=True)
        filepath = os.path.join(my_outdir, base_name.format('all', func_name))
        shared.export_all_available_formats(fig, filepath)

    # background
    data = {
        "graph": {
            "directed": True,
            "metadata": {"background_color": "lightgray"},
            "nodes": [
                {"id": 1, "label": "node a", "metadata": {"size": 30}},
                {"id": 2, "label": "node b", "metadata": {"size": 40}},
                {"id": 3},
                {"id": 4, "label": "node d", "metadata": {"size": 4}},
                {"id": 5, "label": "node e", "metadata": {"shape": "hexagon"}},
            ],
            "edges": [
                {"source": 1, "target": 2},
                {"source": 2, "target": 3},
                {"source": 3, "target": 4},
                {"source": 4, "target": 1},
                {"source": 1, "target": 5},
            ]
        }
    }
    for func_name, func in plotting_functions:
        fig = func(data)
        filepath = os.path.join(my_outdir, base_name.format('background', func_name))
        shared.export_all_available_formats(fig, filepath)

    # node label
    data = {
        "graph": {
            "directed": True,
            "nodes": [
                {"id": 1, "label": "node a", "metadata": {"size": 30}},
                {"id": 2, "label": "node b", "metadata": {"size": 40}},
                {"id": 3},
                {"id": 4, "label": "node d", "metadata": {"size": 4}},
                {"id": 5, "label": "node e", "metadata": {"shape": "hexagon"}},
            ],
            "edges": [
                {"source": 1, "target": 2},
                {"source": 2, "target": 3},
                {"source": 3, "target": 4},
                {"source": 4, "target": 1},
                {"source": 1, "target": 5},
            ]
        }
    }
    for func_name, func in plotting_functions:
        fig = func(data)
        filepath = os.path.join(my_outdir, base_name.format('node_label', func_name))
        shared.export_all_available_formats(fig, filepath)

    # node and edge label
    data = {
        "graph": {
            "directed": True,
            "nodes": [
                {"id": 1, "label": "node a"},
                {"id": 2, "label": "node b"},
                {"id": 3},
                {"id": 4, "label": "node d"},
                {"id": 5, "label": "node e"},
            ],
            "edges": [
                {"source": 1, "target": 2, "label": "e12"},
                {"source": 2, "target": 3},
                {"source": 3, "target": 4, "label": "e34"},
                {"source": 4, "target": 1},
                {"source": 1, "target": 5},
            ]
        }
    }
    for func_name, func in plotting_functions:
        fig = func(data)
        filepath = os.path.join(
            my_outdir, base_name.format('node_label_and_edge_label', func_name))
        shared.export_all_available_formats(fig, filepath)

    # node color
    data = {
        "graph": {
            "directed": True,
            "nodes": [
                {"id": 1, "metadata": {"color": "#f00"}},
                {"id": 2, "metadata": {"color": "green"}},
                {"id": 3},
                {"id": 4, "metadata": {"color": "#0000ff"}},
                {"id": 5, "metadata": {"color": "WRONG"}},
            ],
            "edges": [
                {"source": 1, "target": 2},
                {"source": 2, "target": 3},
                {"source": 3, "target": 4},
                {"source": 4, "target": 1},
                {"source": 1, "target": 5},
            ]
        }
    }
    for func_name, func in plotting_functions:
        fig = func(data)
        filepath = os.path.join(my_outdir, base_name.format('node_color', func_name))
        shared.export_all_available_formats(fig, filepath)

    # node opacity
    data = {
        "graph": {
            "directed": True,
            "nodes": [
                {"id": 1, "metadata": {"opacity": 0.1}},
                {"id": 2, "metadata": {"opacity": 0.5}},
                {"id": 3},
                {"id": 4, "metadata": {"opacity": 1.0}},
                {"id": 5, "metadata": {"opacity": "WRONG"}},
            ],
            "edges": [
                {"source": 1, "target": 2},
                {"source": 2, "target": 3},
                {"source": 3, "target": 4},
                {"source": 4, "target": 1},
                {"source": 1, "target": 5},
            ]
        }
    }
    for func_name, func in plotting_functions:
        fig = func(data)
        filepath = os.path.join(my_outdir, base_name.format('node_opacity', func_name))
        shared.export_all_available_formats(fig, filepath)

    # node size
    data = {
        "graph": {
            "directed": True,
            "nodes": [
                {"id": 1, "metadata": {"size": 20}},
                {"id": 2, "metadata": {"size": 30}},
                {"id": 3},
                {"id": 4, "metadata": {"size": 4}},
                {"id": 5, "metadata": {"size": "WRONG"}},
            ],
            "edges": [
                {"source": 1, "target": 2},
                {"source": 2, "target": 3},
                {"source": 3, "target": 4},
                {"source": 4, "target": 1},
                {"source": 1, "target": 5},
            ]
        }
    }
    for func_name, func in plotting_functions:
        fig = func(data)
        filepath = os.path.join(my_outdir, base_name.format('node_size', func_name))
        shared.export_all_available_formats(fig, filepath)

    # node shape
    data = {
        "graph": {
            "directed": True,
            "nodes": [
                {"id": 1, "metadata": {"shape": "circle"}},
                {"id": 2, "metadata": {"shape": "rectangle"}},
                {"id": 3},
                {"id": 4, "metadata": {"shape": "hexagon"}},
                {"id": 5, "metadata": {"shape": "WRONG"}},
            ],
            "edges": [
                {"source": 1, "target": 2},
                {"source": 2, "target": 3},
                {"source": 3, "target": 4},
                {"source": 4, "target": 1},
                {"source": 1, "target": 5},
            ]
        }
    }
    for func_name, func in plotting_functions:
        fig = func(data)
        filepath = os.path.join(my_outdir, base_name.format('node_shape', func_name))
        shared.export_all_available_formats(fig, filepath)

    # node border color and border size
    data = {
        "graph": {
            "directed": True,
            "nodes": [
                {"id": 1,
                 "metadata": {"shape": "hexagon", "border_color": "red", "border_size": 3}},
                {"id": 2,
                 "metadata": {"shape": "circle", "border_color": "green", "border_size": 3}},
                {"id": 3,
                 "metadata": {"border_color": "green", "border_size": 3}},
                {"id": 4,
                 "metadata": {"shape": "rectangle", "border_color": "blue", "border_size": 3}},
                {"id": 5,
                 "metadata": {"border_color": "WRONG", "border_size": "WRONG"}},
                {"id": 6},
            ],
            "edges": [
                {"source": 1, "target": 2},
                {"source": 2, "target": 3},
                {"source": 3, "target": 4},
                {"source": 4, "target": 1},
                {"source": 1, "target": 5},
                {"source": 1, "target": 6},
            ]
        }
    }
    for func_name, func in plotting_functions:
        fig = func(data)
        filepath = os.path.join(
            my_outdir, base_name.format('node_border_color_and_size', func_name))
        shared.export_all_available_formats(fig, filepath)

    # node image
    png10x10 = gv.convert.image_to_data_url(os.path.join(shared.IN_DIR, 'rectangle_10x10.png'))
    png30x10 = gv.convert.image_to_data_url(os.path.join(shared.IN_DIR, 'rectangle_30x10.png'))
    png10x30 = gv.convert.image_to_data_url(os.path.join(shared.IN_DIR, 'rectangle_10x30.png'))
    png100x50 = gv.convert.image_to_data_url(os.path.join(shared.IN_DIR, 'rectangle_100x50.png'))
    svg10x10 = gv.convert.image_to_data_url(os.path.join(shared.IN_DIR, 'rectangle_10x10.svg'))
    svg30x10 = gv.convert.image_to_data_url(os.path.join(shared.IN_DIR, 'rectangle_30x10.svg'))
    svg10x30 = gv.convert.image_to_data_url(os.path.join(shared.IN_DIR, 'rectangle_10x30.svg'))
    svg100x50 = gv.convert.image_to_data_url(os.path.join(shared.IN_DIR, 'rectangle_100x50.svg'))

    data = {
        "graph": {
            "directed": True,
            "nodes": {
                1: {"metadata": {"shape": "circle", "image": png10x10}},
                2: {"metadata": {"shape": "rectangle", "image": png10x10}},
                3: {"metadata": {"shape": "hexagon", "image": png10x10}},
                4: {"metadata": {"shape": "circle", "image": png30x10}},
                5: {"metadata": {"shape": "rectangle", "image": png30x10}},
                6: {"metadata": {"shape": "hexagon", "image": png30x10}},
                7: {"metadata": {"shape": "circle", "image": png10x30}},
                8: {"metadata": {"shape": "rectangle", "image": png10x30}},
                9: {"metadata": {"shape": "hexagon", "image": png10x30}},
                10: {"metadata": {"shape": "circle", "image": png100x50}},
                11: {"metadata": {"shape": "rectangle", "image": png100x50}},
                12: {"metadata": {"shape": "hexagon", "image": png100x50}},

                13: {"metadata": {"shape": "circle", "image": svg10x10}},
                14: {"metadata": {"shape": "rectangle", "image": svg10x10}},
                15: {"metadata": {"shape": "hexagon", "image": svg10x10}},
                16: {"metadata": {"shape": "circle", "image": svg30x10}},
                17: {"metadata": {"shape": "rectangle", "image": svg30x10}},
                18: {"metadata": {"shape": "hexagon", "image": svg30x10}},
                19: {"metadata": {"shape": "circle", "image": svg10x30}},
                20: {"metadata": {"shape": "rectangle", "image": svg10x30}},
                21: {"metadata": {"shape": "hexagon", "image": svg10x30}},
                22: {"metadata": {"shape": "circle", "image": svg100x50}},
                23: {"metadata": {"shape": "rectangle", "image": svg100x50}},
                24: {"metadata": {"shape": "hexagon", "image": svg100x50}},
                25: {"metadata": {"shape": "circle", "image": 'WRONG'}},
                26: {"metadata": {"shape": "rectangle", "image": 'WRONG'}},
                27: {"metadata": {"shape": "hexagon", "image": 'WRONG'}},
                28: {"metadata": {"image": 'WRONG'}},
                29: {"metadata": {"shape": "WRONG", "image": svg30x10}},
            },
            "edges": [
                {"source": 1, "target": 2},
                {"source": 2, "target": 3},
                {"source": 3, "target": 1},
                {"source": 1, "target": 13},

                {"source": 4, "target": 5},
                {"source": 5, "target": 6},
                {"source": 6, "target": 4},
                {"source": 4, "target": 16},

                {"source": 7, "target": 8},
                {"source": 8, "target": 9},
                {"source": 9, "target": 7},
                {"source": 7, "target": 19},

                {"source": 10, "target": 11},
                {"source": 11, "target": 12},
                {"source": 12, "target": 10},
                {"source": 10, "target": 22},

                {"source": 13, "target": 14},
                {"source": 14, "target": 15},
                {"source": 15, "target": 13},

                {"source": 16, "target": 17},
                {"source": 17, "target": 18},
                {"source": 18, "target": 16},

                {"source": 19, "target": 20},
                {"source": 20, "target": 21},
                {"source": 21, "target": 19},

                {"source": 22, "target": 23},
                {"source": 23, "target": 24},
                {"source": 24, "target": 22},

                {"source": 25, "target": 26},
                {"source": 26, "target": 27},
                {"source": 27, "target": 28},
                {"source": 28, "target": 29},
                {"source": 29, "target": 25},
            ]
        }
    }
    for func_name, func in plotting_functions:
        fig = func(data)
        filepath = os.path.join(
            my_outdir, base_name.format('node_image_and_shape', func_name))
        shared.export_all_available_formats(fig, filepath)

    # node and edge hover
    data = {
        "graph": {
            "directed": True,
            "nodes": [
                {"id": 1, "metadata": {
                    "hover": ("Test node 1 hover which is an example of a long text that goes on"
                              + "   and on"*50
                              + "andon"*200)}},
                {"id": 2, "metadata": {"hover": "Test node 2 hover"}},
                {"id": 3},
                {"id": 4, "metadata": {"hover": "Test node 4 hover"}},
                {"id": 5},
            ],
            "edges": [
                {"source": 1, "target": 2, "metadata": {"hover": "Test edge (1,2) hover"}},
                {"source": 2, "target": 3, "metadata": {"hover": "Test edge (2,3) hover"}},
                {"source": 3, "target": 4},
                {"source": 4, "target": 1, "metadata": {"hover": "Test edge (4,1) hover"}},
                {"source": 1, "target": 5},
            ]
        }
    }
    for func_name, func in plotting_functions:
        fig = func(data)
        filepath = os.path.join(
            my_outdir, base_name.format('node_and_edge_hover', func_name))
        shared.export_all_available_formats(fig, filepath)

    # node and edge click
    data = {
        "graph": {
            "directed": True,
            "nodes": [
                {"id": 1, "metadata": {"click": "Test node 1 click"}},
                {"id": 2, "metadata": {"click": "Test node 2 click"}},
                {"id": 3},
                {"id": 4, "metadata": {
                    "click": "Test node 4 click <ul><li>a: 1</li><li>e: 5</li></ul>"}},
                {"id": 5},
            ],
            "edges": [
                {"source": 1, "target": 2,
                 "metadata": {"click": "Test edge (1,2) click"}},
                {"source": 2, "target": 3,
                 "metadata": {"click": "Test edge (2,3) click"}},
                {"source": 3, "target": 4},
                {"source": 4, "target": 1,
                 "metadata":
                 {"click": "Test edge (4,1) click <ul><li>a: 1</li><li>b: 2</li></ul>"}},
                {"source": 1, "target": 5},
            ]
        }
    }
    for func_name, func in plotting_functions:
        fig = func(data)
        filepath = os.path.join(
            my_outdir, base_name.format('node_and_edge_click', func_name))
        shared.export_all_available_formats(fig, filepath)

    # ----------------------------------------------------------------------------------------
    # edge label
    for directed in [True, False]:
        data = {
            "graph": {
                "directed": directed,
                "nodes": [
                    {"id": 1},
                    {"id": 2},
                    {"id": 3},
                    {"id": 4},
                    {"id": 5},
                ],
                "edges": [
                    {"source": 1, "target": 2, "label": "e12"},
                    {"source": 2, "target": 3, "label": "e23"},
                    {"source": 3, "target": 4},
                    {"source": 4, "target": 1, "label": "e41"},
                    {"source": 1, "target": 5, "label": 42},
                ]
            }
        }
        for func_name, func in plotting_functions:
            fig = func(data)
            suffix = 'directed' if directed else 'undirected'
            filepath = os.path.join(
                my_outdir, base_name.format('edge_label_'+suffix, func_name))
            shared.export_all_available_formats(fig, filepath)

    # edge color
    for directed in [True, False]:
        data = {
            "graph": {
                "directed": directed,
                "nodes": [
                    {"id": 1},
                    {"id": 2},
                    {"id": 3},
                    {"id": 4},
                    {"id": 5},
                ],
                "edges": [
                    {"source": 1, "target": 2, "metadata": {"color": "#f00"}},
                    {"source": 2, "target": 3, "metadata": {"color": "blue"}},
                    {"source": 3, "target": 4},
                    {"source": 4, "target": 1, "metadata": {"color": "#00ff00"}},
                    {"source": 1, "target": 5, "metadata": {"color": "WRONG"}},
                ]
            }
        }
        for func_name, func in plotting_functions:
            fig = func(data)
            suffix = 'directed' if directed else 'undirected'
            filepath = os.path.join(
                my_outdir, base_name.format('edge_color_'+suffix, func_name))
            shared.export_all_available_formats(fig, filepath)

    # edge opacity
    for directed in [True, False]:
        data = {
            "graph": {
                "directed": directed,
                "nodes": [
                    {"id": 1},
                    {"id": 2},
                    {"id": 3},
                    {"id": 4},
                    {"id": 5},
                ],
                "edges": [
                    {"source": 1, "target": 2, "metadata": {"opacity": 0.1}},
                    {"source": 2, "target": 3, "metadata": {"opacity": 0.5}},
                    {"source": 3, "target": 4},
                    {"source": 4, "target": 1, "metadata": {"opacity": 1.0}},
                    {"source": 1, "target": 5, "metadata": {"opacity": "WRONG"}},
                ]
            }
        }
        for func_name, func in plotting_functions:
            fig = func(data)
            suffix = 'directed' if directed else 'undirected'
            filepath = os.path.join(
                my_outdir, base_name.format('edge_opacity_'+suffix, func_name))
            shared.export_all_available_formats(fig, filepath)

    # edge size
    for directed in [True, False]:
        data = {
            "graph": {
                "directed": directed,
                "nodes": [
                    {"id": 1},
                    {"id": 2},
                    {"id": 3},
                    {"id": 4},
                    {"id": 5},
                ],
                "edges": [
                    {"source": 1, "target": 2, "metadata": {"size": 1}},
                    {"source": 2, "target": 3, "metadata": {"size": 2}},
                    {"source": 3, "target": 4},
                    {"source": 4, "target": 1, "metadata": {"size": 3}},
                    {"source": 1, "target": 5, "metadata": {"size": "WRONG"}},
                ]
            }
        }
        for func_name, func in plotting_functions:
            fig = func(data)
            suffix = 'directed' if directed else 'undirected'
            filepath = os.path.join(
                my_outdir, base_name.format('edge_size_'+suffix, func_name))
            shared.export_all_available_formats(fig, filepath)
