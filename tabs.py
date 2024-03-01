import streamlit as st
import json
import uuid
from model import metamodel_dict
import graphviz
from streamlit_agraph import agraph, Node, Edge, Config
import networkx as nx
from graph_function import output_nodes_and_edges, count_nodes, count_edges, find_density, check_path, is_empty, \
    specific_node, is_directed, show_shortest_paths
from streamlit_option_menu import option_menu
def upload_graph():
        uploaded_graph = st.file_uploader("Upload an existing graph", type="json")
        if uploaded_graph is not None:
            uploaded_graph_dict = json.load(uploaded_graph)
            uploaded_nodes = uploaded_graph_dict["nodes"]
            uploaded_edges = uploaded_graph_dict["edges"]
            st.write(uploaded_graph_dict, expanded=False)
        else:
            st.info("Upload Graph Saad Arif")

        update_graph_button = st.button(
            "Update graph via the upload",
            use_container_width=True,
            type="primary"
        )
        if update_graph_button and uploaded_graph is not None:
            st.session_state["node_list"] = uploaded_nodes
            st.session_state["edge_list"] = uploaded_edges
            graph_dict = {
                "nodes": st.session_state["node_list"],
                "edges": st.session_state["edge_list"]
            }
            st.session_state["graph_dict"] = graph_dict


def create_node():
    def print_hi(name, age):
        # Use a breakpoint in the code line below to debug your script.
        st.info(f'Hi, My name is {name} and I am {age} years old')  # Press Strg+F8 to toggle the breakpoint.

    def save_node(name, age, type_n):
        node_dict = {
            "name": name,
            "age": age,
            "id": str(uuid.uuid4()),
            "type": type_n
        }
        st.session_state["node_list"].append(node_dict)

    name_node = st.text_input("Type in the name of the node")
    type_node = st.selectbox("Specify the type of the node", ["Node", "Person"])
    age_node = int(st.number_input("Input the age of the node", value=0))
    print_hi(name_node, age_node)
    save_node_button = st.button("Store node", use_container_width=True, type="primary")
    if save_node_button:
        save_node(name_node, age_node)
    st.write(st.session_state["node_list"])

def create_relation():
    def save_edge(node1, relation, node2):
        edge_dict = {
            "source": node1,
            "target": node2,
            "type": relation,
            "id": str(uuid.uuid4()),
        }
        st.session_state["edge_list"].append(edge_dict)
    # Model logic
    node_list = st.session_state["node_list"]
    node_name_list = []
    for node in node_list:
        node_name_list.append(node["name"])
    # UI Rendering
    node1_col, relation_col, node2_col = st.columns(3)
    with node1_col:
        node1_select = st.selectbox(
            "Select the first node",
            options=node_name_list,
            key="node1_select"
        )
    node2_options = [name for name in node_name_list if name != node1_select]
    # node2_options = []
    # for name in node_name_list:
    #       if name != node1_select:
    #           node2_options.append(name)
    with relation_col:
        # Logic
        relation_list = metamodel_dict["edges"]
        # UI Rendering
        relation_name = st.selectbox(
            "Specify the relation",
            options=relation_list)
    with node2_col:
        node2_select = st.selectbox(
            "Select the second node",
            options=node2_options,
            key="node2_col"
        )
    store_edge_button = st.button("Store Relation",
                                  use_container_width=True,
                                  type="primary")

    if store_edge_button:
        save_edge(node1_select, relation_name, node2_select)

    st.write(f"{node1_select} is {relation_name} {node2_select}")  # Most pythonic version
    st.write(st.session_state["edge_list"])

def store_graph():

    with st.expander("Show Individual lists"):
        st.json(st.session_state["node_list"], expanded=True)
        st.json(st.session_state["edge_list"], expanded=False)

    graph_dict = {
        "nodes": st.session_state["node_list"],
        "edges": st.session_state["edge_list"]
    }
    st.session_state["graph_dict"] = graph_dict

    with st.expander("show graph JSON", expanded=False):
        st.json(st.session_state["graph_dict"])

def Visualize_graph():
    # Create a graphlib graph object
    with st.expander("Graphviz Visualization"):
        graph = graphviz.Digraph()
        graph_dict = {
            "nodes": st.session_state["node_list"],
            "edges": st.session_state["edge_list"]
        }
        st.session_state["graph_dict"] = graph_dict
        node_list = graph_dict["nodes"]
        edge_list = graph_dict["edges"]
        for node in node_list:
            node_name = node["name"]
            graph.node(node_name)
        for edge in edge_list:
            source = edge["source"]
            target = edge["target"]
            label = edge["type"]
            graph.edge(source, target, label)
        st.graphviz_chart(graph)
    with st.expander("Show Graph in AGraph"):
        graph_visualisation_nodes = []
        graph_visualisation_edges = []
        for node in st.session_state["node_list"]:
            graph_visualisation_nodes.append(
                Node(
                    id=node["name"],
                    label=node["name"],
                    size=25,
                    shape="circularImage",
                    image="https://t4.ftcdn.net/jpg/00/65/77/27/360_F_65772719_A1UV5kLi5nCEWI0BNLLiFaBPEkUbv5Fv.jpg")
            )  # includes **kwargs
        for edge in st.session_state["edge_list"]:
            graph_visualisation_edges.append(Edge(
                source=edge["source"],
                label=edge["type"],
                target=edge["target"],
                # **kwargs
            )
            )
        config = Config(width=500,
                        height=500,
                        directed=True,
                        physics=True,
                        hierarchical=True,
                        # **kwargs
                        )

        return_value = agraph(nodes=graph_visualisation_nodes,
                              edges=graph_visualisation_edges,
                              config=config)
    # with st.expander("Streamlit Visualization"):

def Analyze_graph():
    G = nx.Graph()
    graph_dict = st.session_state["graph_dict"]
    node_list = graph_dict["nodes"]
    edge_list = graph_dict["edges"]
    node_tuple_list = []
    edge_tuple_list = []

    for node in node_list:
        node_tuple = (node["name"], node)
        node_tuple_list.append(node_tuple)

    for edge in edge_list:
        edge_tuple = (edge["source"], edge["target"], edge)
        edge_tuple_list.append(edge_tuple)

    G.add_nodes_from(node_tuple_list)
    G.add_edges_from(edge_tuple_list)
    st.write(G.nodes)
    st.write(G.edges)

    select_function = st.selectbox(label="Select function",
                                   options=["Output nodes and edges",
                                            "Count Nodes",
                                            "Count Edges",
                                            "Density of Graph",
                                            "Check Path",
                                            "Check if Graph is Empty",
                                            "Shortest path"])
    if select_function == "Output nodes and edges":
        output_nodes_and_edges(graph=G)
    elif select_function == "Count Nodes":
        count_nodes(graph=G)
    elif select_function == "Count Edges":
        count_edges(graph=G)
    elif select_function == "Density of Graph":
        find_density(graph=G)
    elif select_function == "Check Path":
        check_path(graph=G)
    elif select_function == "Check if Graph is Empty":
        is_empty(graph=G)
    elif select_function == "Is Graph Directed":
        is_directed(graph=G)
    elif select_function == "Specific Node":
        specific_node(graph=G)
    elif select_function == "Shortest path":
        show_shortest_paths(graph=G)
def export_graph():
    graph_string = json.dumps(st.session_state["graph_dict"])

    st.download_button(
        "Export graph to JSON",
        file_name="graph.json",
        mime="application/json",
        data=graph_string,
        use_container_width=True,
        type="primary"
    )