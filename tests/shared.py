import inspect
import os
from copy import deepcopy


def get_path_of_this_file():
    # https://stackoverflow.com/questions/2632199/how-do-i-get-the-path-of-the-current-executed-file-in-python
    return os.path.abspath(inspect.getsourcefile(lambda _: None))


TESTFILE_DIR = os.path.dirname(get_path_of_this_file())
IN_DIR = os.path.join(TESTFILE_DIR, 'in')


def construct_testdata_gjgf():
    # undirected graph
    ug = {
        "graph": {
          "directed": False,
          "nodes": [
            {"id": "0"},
            {"id": "1"},
            {"id": "2"},
            {"id": "3"},
            {"id": "4"},
          ],
          "edges": [
            {"source": "0", "target": "1"},
            {"source": "1", "target": "2"},
            {"source": "0", "target": "2"},
            {"source": "1", "target": "3"},
            {"source": "3", "target": "1"},
            {"source": "1", "target": "4"},
          ]
        }
    }
    # directed graph
    dg = deepcopy(ug)
    dg['graph']['directed'] = True

    # undirected graph with attributes
    uga = {
        "graph": {
          "directed": False,
          "label": "Undirected graph with attributes",
          "metadata": {
            "arrowSize": 6.0,
            "arrowColor": "red",
            "backgroundColor": "lightblue",
            'node_color': "blue",
            "node_opacity": 0.7,
            "node_size": 10,
            "node_shape": "rectangle",
            "node_border_color": "magenta",
            "node_border_size": 2,
            "node_label_color": "green",
            "node_label_size": 6,
            "node_hover": "General node hover",
            "node_click": "General node click",
            "node_image": (
              'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAE8AAABPCAYAAACqNJiGAAAABHNCSVQICAgI'
              'fAhkiAAAAAlwSFlzAAAewgAAHsIBbtB1PgAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPB'
              'oAAAVxSURBVHic7ZhLSFRfHMe/M5qlWTpORRrUIqyGNlIJZdogGPRc9MCikFJEoahpET0oigSJqIVU0tLS'
              'CFrYok2Q0cpJxTKoZkYserioCCZndKzMxvNf/Lhcx3vn0fwuxB9+H7ice8/zN5+595x7rg1KKQhpYf/XAf'
              'yfEXkMRB4DkcdA5DEQeQxEHgORx0DkMRB5DEQeA5HHQOQxEHkMRB4DkcdA5DEQeQxEHgORx0DkMRB5DEQe'
              'A5HHQOQxEHkMRB4DkcdA5DEQeQwyE5aGQsCLF3S8egX8/g1s2wYcPpy856Eh4OpVwOsFRkaAZcuAPXuA48'
              'eB2bOtiR4AlALevdPj/PSJ8ltagKKi5O3v3QPa2oBAgOIqKaEY3e6UBlemx+XLCjabAhB7eDzm9acfXV0K'
              'OTlUv6BAweVSmDWLrtetUxgbS95HqsfSpcYYAYXBwcTtpqYUamqors2mUFyssGSJft3SknzsuAXnzink5S'
              'lUViqcPKmwcWNq8oJBEgYonD6tMDFB+cPDCiUllF9XZ508h0Nh+XKF6mqF5ubU5d26RfUWLFDo6dHz795V'
              'yMxUsNsV+vrSlDc6Sv+Odl1fn5q8ixep3oYNse2VUvD7KaiMDIX3762RFw7r5xMTqcn780ehqIjq3bljLP'
              'd4qGzHjoRjx18w5s0DbLYUnvsZdHZS2tBgbO9yARUVQDQKPHig5w8MAI2NwLFjQCRi7DMaBc6coTpdXbFl'
              '8+f/fYxeL/D5M5CXB+zfbyxvaKD08WMgHI7bjbWrbSQC+Hx0XlZmXqeigtLeXj2vpIQm+ps3gSNHjG2amo'
              'ArV4CeHqC8nB9nXx+lpaVAVpax3OUCnE5aIAcG4nZjrby3b2n1A4DCQvM6Wv7Q0LQo7EB7O62OHR20+mk8'
              'fQo0NwNz5wL37wPZ2fw4tbHjxWizmcc5A2vljYxQmpVFj70ZTieloVBs/qJF9NqQkUGPr98PfPsG1NTQY9'
              'vaSneEFWhja7GYUVBAqfabTLBW3q9flMYTB9A8AwA/fhjL3G7gwgVgfByorgYOHqS56dAhOv5FnD9/xq2S'
              '+CX5b5kzh9LRUXp8zRYc7V/PyTHv4/x5oLubFgafDyguBm7csDTMmDjjoS0UCaYJa+88h4PSyUnzVRMAvn'
              '+nND8/TkR2YPt2/bqxMfEdkg7a2FosZmhl2m8ywVp5xcX63fbli3kdLX/FCvPyN2+As2eBzEwSeelSwkk7'
              'LbSx48WoVPI4YbW83Fxg9Wo6f/bMvE53N6Xr1xvLxseBfftonmlqone7sTHK0+YpK9DG7u+n15GZBAJAME'
              'gL35o1CTpK9U3+b3cYZWXGHUYgoO8wPnwwtq2tpbabNytEowqTkwrl5ZR39GjyGNPZYbS3G8tPnEhphxFf'
              'XjhMG3zt2LqVOty1KzY/EoltFwzSfhNQOHVK39t+/KjvbWtrjeN1dFDZ4sUKX7/q+cPDCk4nlXV2Gtv5fH'
              'osjx7p8tra9Pznz43tWlv1va3XS3lTUxSHtrft7U1TXn+/+deKmYffb2w7/auKw6GwahUFBCiUltK+eXr9'
              'wUGF3FwKuKvL2N/Dh/SlIz/feMfW1SWPsbLS2Of0ryoAfVwoLKRzuz2lryrxX1UWLtT3eIkwWzWrqoCXL4'
              'Fr12iOC4WAtWuBvXvpBXjm97wnT4ADB6hOVZWxv507gevXgdevqW59vV7mdtPikoiVK415NhvtarZsAW7f'
              'pnkuOxvYvRvweIBNm5L+dBvdfkI6yGd4BiKPgchjIPIYiDwGIo+ByGMg8hiIPAYij4HIYyDyGIg8BiKPgc'
              'hjIPIYiDwGIo+ByGMg8hiIPAYij4HIYyDyGIg8BiKPgchjIPIYiDwGIo/Bf5DMXNIIfe3zAAAAAElFTkSu'
              'QmCC'),
            "node_x": 1.0,
            "edge_color": "orange",
            'edge_opacity': 0.7,
            "edge_size": 2.5,
            "edge_label_color": "cyan",
            "edge_label_size": 4,
            "edge_hover": "General edge hover",
            "edge_click": "General edge click",
            "other_metadata": 42,
          },
          "nodes": [
            {
              "id": "0",
              "type": "Individual node type",
              "label": "Individual node 0 label",
              "metadata": {
                  "color": "black",
                  "opacity": 1.0,
                  "size": 30,
                  "shape": "circle",
                  "borderColor": "white",
                  "borderSize": 1,
                  "labelColor": "black",
                  "labelSize": 10,
                  "hover": "Individual node hover",
                  "click": "Individual node click",
                  "image": (
                    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAE8AAADsCAYAAAA1vPvGAAAABHNCSV'
                    'QICAgIfAhkiAAAAAlwSFlzAAAewgAAHsIBbtB1PgAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYX'
                    'BlLm9yZ5vuPBoAAAmpSURBVHic7dp5cJT1AcbxZ4/cJ4SEJgQJCISrFFRQEG1xCrUDg1UZmEJLa6'
                    '0KCJ0iY3UUKJViFZyhpYAUFRxapHKPYhGNlLOJlXAVAkgQgRwkIcnm2N1sNrvbP97shmV3E8nDTK'
                    'czz+e/vL99d9/97vv+3mNi8p0e5IN0ivl/vQH/zxSPoHgExSMoHkHxCIpHUDyC4hEUj6B4BMUjKB'
                    '5B8QiKR1A8guIRFI+geATFIygeQfEIikdQPILiERSPoHgExSMoHkHxCNZIA/knnfiswI6jZ5worW'
                    'hBTZ0H0VEmDOwTjUe/n4xpE1JgaSf9pVI3VmysxqFCBxodXvTIsGLy+GQ8M6ULoqym2/olSircKD'
                    'zThMKiJlRUtwAAXpmTju5pEb9ewI68eqzfYUPxlWZYrSYMGxCLOT/uivu+E9fhuqZI/583avolFJ'
                    'x0Bv6OjjKh2d320tHD4vHRmz2RmmQJWffgUQcmPnsFDXYvEuPNSEu1oOSaGx4vcP/weHzy1h2Ij7'
                    '09O33/CcW4cLk5ZPm53X2RmxPd7rpPLy7HW9tqAQBZGVY0u324XuuBxQysWpCJmVO6tLt+xG8wfn'
                    'Qi1izMxOldd8J+dABcxwfi+uFcrF2UicR4M/51woHn36gIWc/W4MHkeVfRYPfi1z/tiqpDufj6k3'
                    '44/1FfDOkXgyPHHXhuWeh6nXW91oPs7lF45KEk/HZ2+jde7+3tNry1rRZdUyzY/24OSvf1R8WBXL'
                    'yzJAsAMHfpNRwramr3PSLuee35y5ZazHylHEkJZtQVDIDphqNwydoqLFpVhZHfjkP+pt4w3/DznC'
                    'l2YehjF2E2mVC8py96ZUXd6keHqLZ5kJZq7P3Nbh9ihp8F0P6e5/ECOeMuoKTCjfVLsvDEo6lB43'
                    'NfvYZV79XgkYeSsGtlz4if3alj596hxnzgcHrR4gluv3VvPQBg5pQuQeEAYHDfGDxwVzxaPD7syK'
                    'sPLD9T7MKLKyqxYGUlHE3ekM/zeoGl667jxRWVOFToCBrzh7sV+SccKKlwIyXRjOkTU0LG/Yfrx4'
                    'cbUd8Yuj1+nYp37KyxOw/uGxs0+Tc6vDhd7AJgzG3hjLnLWJ5/w3w6sE8MCoucWLruOuYsvRayzt'
                    'J1VViwshK7DzTg7sGxndnkIAWnjM++Z0gcoqNCT16D7oxB1xQLXM0+FBY5Q8b9bine9VoP3t1lw/'
                    'xlFYiOMuG1eRlB4xcuN8PXuiNmpoc/02VlGIfq+Uttk7zZDPzttR7ITLdiw04bNn5QFxjb/4Udv1'
                    'tThfhYM95/I/u2nGjOXzJ+4KwI22gytW3/l1+Hnoz8OjyXr9xUg8Wrq9Dk8sLpMsqMG5WAV+ZkhJ'
                    'zObQ0eAMaZOSkh/Jf0H2a19Z6g5d3TrNj0eg+M++VlzF5SjhFDYpGWasH0F0rh8QKrXv4WBveN6W'
                    'hzvxFbg3Eodk2JfMhH2s4bdfgzpiZZ0Cc7Cjk9ohEbY+ziBaec2LK3PujSBQCcTcbfkcIBQHLrmN'
                    'MVOpeMHZmARbPSYXd6MWV+CX7yQinKKlswY1JKyKTOaGrdCZITI8dLaR3z7zDhdLjnzZiUghmT2i'
                    'bVvUcaMffVa1ixsRrlVW5sXp4dGIuLNeI22CNPsvWtY3Ex4QMveCYdBwsd+KzAjtMXXBjYJwZrFm'
                    'Z2tJm3xL8T1DdG3qv8Y3ExkS/ob3kC+cH9ifhw9R2wmIG/76nHfy64AmP+C+Zmty9iwGqbsVFdks'
                    'P/6mYzMPG7SYG/n3wsFQlxt/cuMjXJeL+ausjxquva306gk2fb3Jxo5PY25p/jZ9suJPv1ig5c85'
                    'VXtYRdt6zSbbxH7/DXYKe+bMJLf6yA1WKC2QwsXlOF8+1M2p3RP8fY9rII2+jzAWWVLa2vjXyXQv'
                    '+kPl/bnJAYb8aQ1kn9yHFH2NcfPmYsv29o6L1jo8OLqfNL4XT58PtfpeOlp7q1LisJzFO3w6jWE9'
                    '3R086QeRsAii66Avfydw+KfI/bqXifn3Li7FfG4XrP4OA3nzw+GQCwblstfDdt19mvXDh0zAGrxY'
                    'THxyWHvO/sJeU4d8mFh8ck4vknumHxsxl48J54nDzfhHmvh17/ddaoYfHokWFFXaMXm/9RFzK+bq'
                    'txv/vwmEQkJ0ZOFHbkn/+2Y9pvSrH7QAMul7nhbvGhxePDlXI3lm+oxoTZV+DzARMeTAy5fJg7vS'
                    'vSUi0oOOnE/OUVgT3m4tVmTJ1fAq8X+PmPUkJuzTbstOGvH9YhK8OKjX/oAbMZsJiB95ZlI72LBW'
                    'u31GLLx/W4WdFFF/Ly7cjLt2Pf5/bA8vwTjsDywpvuUS1mYNEs4z54/vIKHDhqHA1eL7B+pw2rN9'
                    'fAYgYWzuwWMRwQ4d7203w7xj91OejDAOOe0G/syATs+FN22Kcq+7+wY9Kcq2GfqoweZjxVufEkUH'
                    'TRhRFTL8HV7EXeO73wvREJQe+351AjJsy+gqQEM45t7YM7e7bNQ08uLMP6nbZ2v+TYkQnYt75X0D'
                    'KfD3h6cRne3m6sm5VhhavZh2qb8VTlzy9nYtbU9p+qhI3ndPmQl9+IvHw7Tn3pQkV1C1zNPnRJNm'
                    'Nobiwmj0vGDx9IDHogcDP/87yDR43nedndrXh8XDJmTg19nrdyUw3OFLtw79A4/CLC9dyb79fixL'
                    'kmDB8YG/SoaOMHdRHnV7/cnGg897O0sGPbP63Hhp3G8zyLxXieN3ca+TxPOqbH8ATFIygeQfEIik'
                    'dQPILiERSPoHgExSMoHkHxCIpHUDyC4hEUj6B4BMUjKB5B8QiKR1A8guIRFI+geATFIygeQfEIik'
                    'dQPILiERSPoHgExSMoHkHxCIpHUDyC4hEUj6B4BMUjKB5B8QiKR1A8guIRFI+geATFIygeQfEIik'
                    'dQPILiERSPoHgExSMoHkHxCIpHUDyC4hEUj6B4BMUjKB5B8QiKR1A8guIRFI+geATFIygeQfEIik'
                    'dQPILiERSPoHgExSMoHkHxCIpHUDyC4hEUj6B4BMUjKB5B8QiKR1A8guIRFI+geATFIygeQfEIik'
                    'dQPILiERSPoHgExSMoHkHxCIpHUDyC4hEUj6B4BMUjKB5B8QiKR1A8guIRFI+geATFIygeQfEIik'
                    'dQPILiERSPoHgExSMoHkHxCIpHUDyC4hEUj6B4BMUjKB5B8QiKR1A8guIRFI+geATFIygeQfEIik'
                    'dQPILiERSPoHgExSMoHkHxCIpHUDyC4hEUj6B4BMUjKB5B8QiKR1A8guIRFI+geATFIygeQfEIik'
                    'dQPILiERSPoHgExSMoHkHxCIpHUDyC4hEUj6B4BMUjKB7hvzwh55xqT4cwAAAAAElFTkSuQmCC'),
                  "x": 0.5,
                  "y": 0.5,
                  "other_metadata": 42,
                }
            },
            {
              "id": "1",
              "label": "Individual node 1 label",
            },
            {
              "id": "2",
            },
            {
              "id": "3",
              "label": "Individual node 3 label",
            },
            {
              "id": "4",
            },
          ],
          "edges": [
            {
              "source": "0",
              "relation": "Individual edge relationship",
              "target": "1",
              "directed": False,
              "label": "Individual edge label",
              "metadata": {
                  "color": "black",
                  "opacity": 1.0,
                  "size": 4.0,
                  "labelColor": "black",
                  "labelSize": 12,
                  "hover": "Individual edge hover",
                  "click": "Individual edge click",
                  "other_metadata": 42,
              }
            },
            {
              "source": "1",
              "target": "2",
            },
            {
              "source": "0",
              "target": "2",
              "label": "Individual edge (0,2) label",
            },
            {
              "source": "1",
              "target": "3",
            },
            {
              "source": "3",
              "target": "1",
              "label": "Individual edge (3,1) label",
            },
            {
              "source": "1",
              "target": "4",
            }
          ]
        }
    }
    # directed graph with attributes
    dga = deepcopy(uga)
    dga['graph']['directed'] = True
    dga['graph']['label'] = 'Directed graph with attributes'

    testdata = {
        'undirected': ug,
        'directed': dg,
        'undirected attributed': uga,
        'directed attributed': dga,
        'multiple': {'graphs': [ug['graph'], dg['graph'], uga['graph'], dga['graph']]},
    }
    return testdata


def construct_testdata_graph_tool():
    try:
        import graph_tool as gt

        # undirected graph
        ug = gt.Graph(directed=False)
        v1 = ug.add_vertex()
        v2 = ug.add_vertex()
        v3 = ug.add_vertex()
        e1 = ug.add_edge(v1, v2)
        e2 = ug.add_edge(v2, v3)
        e3 = ug.add_edge(v3, v1)
        # directed graph
        dg = gt.Graph(directed=True)
        v1 = dg.add_vertex()
        v2 = dg.add_vertex()
        v3 = dg.add_vertex()
        e1 = dg.add_edge(v1, v2)
        e2 = dg.add_edge(v2, v3)
        e3 = dg.add_edge(v3, v1)
        # undirected graph with attributes
        uga = gt.Graph(directed=False)
        v1 = uga.add_vertex()
        v2 = uga.add_vertex()
        v3 = uga.add_vertex()
        e1 = uga.add_edge(v1, v2)
        e2 = uga.add_edge(v2, v3)
        e3 = uga.add_edge(v3, v1)
        uga.graph_properties['label'] = uga.new_graph_property('string')
        uga.graph_properties['label'] = 'Undirected graph with attributes'
        uga.graph_properties['node_color'] = uga.new_graph_property('string')
        uga.graph_properties['node_color'] = 'green'
        uga.graph_properties['edge_opacity'] = uga.new_graph_property('double')
        uga.graph_properties['edge_opacity'] = 0.5
        uga.vertex_properties['size'] = uga.new_vertex_property('int')
        uga.vertex_properties['size'][v1] = 50
        uga.vertex_properties['color'] = uga.new_vertex_property('string')
        uga.vertex_properties['color'][v1] = 'red'
        uga.edge_properties['size'] = uga.new_edge_property('int')
        uga.edge_properties['size'][e1] = 10
        uga.edge_properties['color'] = uga.new_edge_property('string')
        uga.edge_properties['color'][e1] = 'blue'
        # directed graph with attributes
        dga = gt.Graph(directed=True)
        v1 = dga.add_vertex()
        v2 = dga.add_vertex()
        v3 = dga.add_vertex()
        e1 = dga.add_edge(v1, v2)
        dga.add_edge(v2, v3)  # e2
        dga.add_edge(v3, v1)  # e3
        dga.graph_properties['label'] = dga.new_graph_property('string')
        dga.graph_properties['label'] = 'Directed graph with attributes'
        dga.graph_properties['node_color'] = dga.new_graph_property('string')
        dga.graph_properties['node_color'] = 'green'
        dga.graph_properties['edge_opacity'] = dga.new_graph_property('double')
        dga.graph_properties['edge_opacity'] = 0.5
        dga.vertex_properties['size'] = dga.new_vertex_property('int')
        dga.vertex_properties['size'][v1] = 50
        dga.vertex_properties['color'] = dga.new_vertex_property('string')
        dga.vertex_properties['color'][v1] = 'red'
        dga.edge_properties['size'] = dga.new_edge_property('int')
        dga.edge_properties['size'][e1] = 10
        dga.edge_properties['color'] = dga.new_edge_property('string')
        dga.edge_properties['color'][e1] = 'blue'
        testdata = {
            'undirected': ug,
            'directed': dg,
            'undirected attributed': uga,
            'directed attributed': dga,
        }
    except Exception as excp:
        print('Graph creation error:', excp)
        testdata = None
    return testdata


def construct_testdata_igraph():
    try:
        import igraph as ig

        # undirected graph
        ug = ig.Graph(directed=False)
        ug.add_vertex()
        ug.add_vertex()
        ug.add_vertex()
        ug.add_edge(0, 1)
        ug.add_edge(1, 2)
        ug.add_edge(2, 0)
        # directed graph
        dg = ig.Graph(directed=True)
        dg.add_vertex()
        dg.add_vertex()
        dg.add_vertex()
        dg.add_edge(0, 1)
        dg.add_edge(1, 2)
        dg.add_edge(2, 0)
        # undirected graph with attributes
        uga = ig.Graph(directed=False)
        uga.add_vertex()
        uga.add_vertex()
        uga.add_vertex()
        uga.add_edge(0, 1)
        uga.add_edge(1, 2)
        uga.add_edge(2, 0)
        uga['label'] = 'Undirected graph with attributes'
        uga['node_color'] = 'green'
        uga['edge_opacity'] = 0.5
        uga.vs[0]['size'] = 50
        uga.vs[0]['color'] = 'red'
        uga.es[0]['size'] = 10
        uga.es[0]['color'] = 'blue'
        # directed graph with attributes
        dga = ig.Graph(directed=True)
        dga.add_vertex()
        dga.add_vertex()
        dga.add_vertex()
        dga.add_edge(0, 1)
        dga.add_edge(1, 2)
        dga.add_edge(2, 0)
        dga['label'] = 'Directed graph with attributes'
        dga['node_color'] = 'green'
        dga['edge_opacity'] = 0.5
        dga.vs[0]['size'] = 50
        dga.vs[0]['color'] = 'red'
        dga.es[0]['size'] = 10
        dga.es[0]['color'] = 'blue'
        testdata = {
            'undirected': ug,
            'directed': dg,
            'undirected attributed': uga,
            'directed attributed': dga,
        }
    except Exception as excp:
        print('Graph creation error:', excp)
        testdata = None
    return testdata


def construct_testdata_networkit():
    try:
        import networkit as nk

        # undirected graph
        ug = nk.Graph(directed=False)
        ug.addNode()
        ug.addNode()
        ug.addNode()
        ug.addEdge(0, 1)
        ug.addEdge(1, 2)
        ug.addEdge(2, 0)
        # directed graph
        dg = nk.Graph(directed=True)
        dg.addNode()
        dg.addNode()
        dg.addNode()
        dg.addEdge(0, 1)
        dg.addEdge(1, 2)
        dg.addEdge(2, 0)
        # undirected graph with attributes - not supported, workaround with dicts
        uga = [ug, dict(node_color='green'),
               {0: dict(color='red')}, {'(0, 1)': dict(color='blue')}]
        # directed graph with attributes - not supported, workaround with dicts
        dga = [dg, dict(node_color='green'),
               {0: dict(color='red')}, {'(0, 1)': dict(color='blue')}]
        testdata = {
            'undirected': ug,
            'directed': dg,
            'undirected attributed': uga,
            'directed attributed': dga,
        }
    except Exception as excp:
        print('Graph creation error:', excp)
        testdata = None
    return testdata


def construct_testdata_networkx():
    try:
        import networkx as nx

        # undirected graph
        ug = nx.Graph()
        ug.add_node(0)
        ug.add_node(1)
        ug.add_node(2)
        ug.add_edge(0, 1)
        ug.add_edge(1, 2)
        ug.add_edge(2, 0)
        # directed graph
        dg = nx.DiGraph()
        dg.add_node(0)
        dg.add_node(1)
        dg.add_node(2)
        dg.add_edge(0, 1)
        dg.add_edge(1, 2)
        dg.add_edge(2, 0)
        # undirected graph with attributes
        uga = nx.Graph()
        uga.add_node(0)
        uga.add_node(1)
        uga.add_node(2)
        uga.add_edge(0, 1)
        uga.add_edge(1, 2)
        uga.add_edge(2, 0)
        uga.graph['label'] = 'Undirected graph with attributes'
        uga.graph['node_color'] = 'green'
        uga.graph['edge_opacity'] = 0.5
        uga.nodes[0]['size'] = 50
        uga.nodes[0]['color'] = 'red'
        uga.edges[(0, 1)]['size'] = 10
        uga.edges[(0, 1)]['color'] = 'blue'
        # directed graph with attributes
        dga = nx.DiGraph()
        dga.add_node(0)
        dga.add_node(1)
        dga.add_node(2)
        dga.add_edge(0, 1)
        dga.add_edge(1, 2)
        dga.add_edge(2, 0)
        dga.graph['label'] = 'Directed graph with attributes'
        dga.graph['node_color'] = 'green'
        dga.graph['edge_opacity'] = 0.5
        dga.nodes[0]['size'] = 50
        dga.nodes[0]['color'] = 'red'
        dga.edges[(0, 1)]['size'] = 10
        dga.edges[(0, 1)]['color'] = 'blue'
        # directed graph with more attributes
        dga2 = nx.DiGraph()
        dga2.graph['node_label_size'] = 14
        dga2.graph['node_label_color'] = 'green'
        dga2.graph['edge_label_size'] = 10
        dga2.graph['edge_label_color'] = 'blue'
        dga2.add_node(0, label='first node', color='red', size=15, shape='rectangle', opacity=0.7,
                      label_color='red', label_size=20, border_color='black', border_size=3)
        dga2.add_node(3, color='green', size=15, shape='hexagon', opacity=0.7,
                      label_color='green', label_size=10, border_color='blue', border_size=3)
        dga2.add_node(6, label='last node')
        dga2.add_edge(0, 1)
        dga2.add_edge(1, 2, label='e2')
        dga2.add_edge(2, 3)
        dga2.add_edge(3, 4)
        dga2.add_edge(4, 5, label='e5', color='orange', label_color='gray', label_size=14,
                      size=4.0)
        dga2.add_edge(5, 6)
        dga2.add_edge(6, 2, label='e7')
        testdata = {
            'undirected': ug,
            'directed': dg,
            'undirected attributed': uga,
            'directed attributed': dga,
            'directed attributed 2': dga2,
        }
    except Exception as excp:
        print('Graph creation error:', excp)
        testdata = None
    return testdata


def construct_testdata_pyntacle():
    try:
        # Uses igraph internally, hence same data can be used
        testdata = construct_testdata_igraph()
    except Exception as excp:
        print(excp)
        testdata = None
    return testdata


def construct_testdata_snap():
    try:
        import snap

        # undirected graph
        ug = snap.TUNGraph.New()
        ug.AddNode(0)
        ug.AddNode(1)
        ug.AddNode(2)
        ug.AddEdge(0, 1)
        ug.AddEdge(1, 2)
        ug.AddEdge(2, 0)
        # directed graph
        dg = snap.TNGraph.New()
        dg.AddNode(0)
        dg.AddNode(1)
        dg.AddNode(2)
        dg.AddEdge(0, 1)
        dg.AddEdge(1, 2)
        dg.AddEdge(2, 0)
        # undirected graph with attributes - not supported
        # directed graph with attributes - caution: graph properties not supported
        dga = snap.TNEANet.New()
        dga.AddNode(0)
        dga.AddNode(1)
        dga.AddNode(2)
        dga.AddEdge(0, 1)
        dga.AddEdge(1, 2)
        dga.AddEdge(2, 0)
        dga.AddFltAttrN('size')
        dga.AddIntAttrN('label_size')
        dga.AddStrAttrN('color')
        dga.AddFltAttrDatN(0, 50.0, 'size')
        dga.AddIntAttrDatN(0, 10, 'label_size')
        dga.AddStrAttrDatN(0, 'red', 'color')
        dga.AddFltAttrE('size')
        dga.AddIntAttrE('label_size')
        dga.AddStrAttrE('color')
        dga.AddFltAttrDatE(0, 10.0, 'size')
        dga.AddIntAttrDatE(0, 10, 'label_size')
        dga.AddStrAttrDatE(0, 'blue', 'color')
        testdata = {
            'undirected': ug,
            'directed': dg,
            'directed attributed': dga,
        }
    except Exception as excp:
        print('Graph creation error:', excp)
        testdata = None
    return testdata


TESTDATA_GJGF = construct_testdata_gjgf()
TESTDATA_GRAPH_TOOL = construct_testdata_graph_tool()
TESTDATA_IGRAPH = construct_testdata_igraph()
TESTDATA_NETWORKIT = construct_testdata_networkit()
TESTDATA_NETWORKX = construct_testdata_networkx()
TESTDATA_PYNTACLE = construct_testdata_pyntacle()
TESTDATA_SNAP = construct_testdata_snap()


def export_all_available_formats(fig, filepath, overwrite=True):
    if not filepath.endswith('.html'):
        filepath += '.html'
    fig.export_html(filepath, overwrite=overwrite)
