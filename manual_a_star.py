from A_star import *


tree_plotter = Tree()

tree_plotter.add_node(None, "E1")
tree_plotter.plot_tree()

tree_plotter.add_node("E1", "E2")
tree_plotter.plot_tree()

tree_plotter.add_node("E1", "E3")
tree_plotter.plot_tree()

tree_plotter.add_node("E2", "E4")
tree_plotter.plot_tree()

tree_plotter.add_node("E2", "E5")
tree_plotter.plot_tree()

tree_plotter.add_node("E3", "E6")
tree_plotter.plot_tree()

tree_plotter.add_node("E3", "E7")
tree_plotter.plot_tree()