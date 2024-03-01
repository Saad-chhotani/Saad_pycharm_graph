import streamlit as st
import json
from streamlit_option_menu import option_menu
from tabs import (upload_graph,
                  create_node,
                  create_relation,
                  store_graph,
                  Visualize_graph,
                  Analyze_graph, export_graph)

if __name__ == '__main__':
    st.set_page_config(layout="wide", initial_sidebar_state="expanded")

    if "node_list" not in st.session_state:
        st.session_state["node_list"] = []
    if "edge_list" not in st.session_state:
        st.session_state["edge_list"] = []
    if "graph_dict" not in st.session_state:
        st.session_state["graph_dict"] = []

    st.title("PyInPSE Tutorial 1")
    tab_list = [
     "Import Graph",
     "Create Nodes",
     "Create Relations between nodes",
     "Store the Graph",
     "Visualize the graph",
     "Analyze the graph",
     "Export the Graph"
     ]

    with st.sidebar:
        pass
        selected_tab = option_menu("Main Menu",
                                   tab_list,
                                   icons=['house', 'gear', "arrow-clockwise"],
                                   menu_icon="cast",
                                   default_index=0,
                                   orientation="vertical"
                                   )
    # selected_tab = option_menu("Main Menu",
    #                  tab_list,
    #                  icons=['house', 'gear', "arrow-clockwise"],
    #                  menu_icon="cast",
    #                  default_index=1,
    #                          orientation = "horizontal"
    #                  )

    if selected_tab == "Import Graph":
        upload_graph()

    if selected_tab == "Create Nodes":
        create_node()

    if selected_tab == "Create Relations between nodes":
        create_relation()

    if selected_tab == "Store the Graph":
        store_graph()

    if selected_tab == "Visualize the graph":
        Visualize_graph()

    if selected_tab == "Analyze the graph":
        Analyze_graph()


    if selected_tab == "Export the Graph":
        export_graph()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
