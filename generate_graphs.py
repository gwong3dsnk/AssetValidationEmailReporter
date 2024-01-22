import os, helper
import matplotlib.pyplot as plt
import seaborn as sns


class GenerateGraphs:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.csv_graph_path = f"{csv_file_path.rpartition('/')[0]}/Graphs"
        self.csv_file_name = csv_file_path.rpartition("/")[2].replace(".csv", "")

        # Verify that a Graph subdirectory exists under the current date directory.
        helper.graph_directory_exists(f"{self.csv_graph_path}/{self.csv_file_name}")

        # self.view_plots_in_explorer()

    def make_bar_plot(self, *args):
        """
        Called by generate_graph_data to make a bar plot.
        :param args: data_type_name, x_axis_data, y_axis_data, bar_colors
        :return:
        """

        fig, ax = plt.subplots()
        bar_values = ax.bar(args[1], args[2])
        sns.barplot(x=args[1], y=args[2], hue=args[1], legend=False, palette=args[3])
        ax.grid(axis="y")
        ax.set(ylabel=f"{args[0]} Count", xlabel=f"{args[0]} Type", axisbelow=True)
        ax.bar_label(bar_values)
        plt.title(f"Asset {args[0]} Count")

        plot_file_path = self.save_plot_as_img(args[0])
        return plot_file_path

    def make_pie_chart(self, *args):
        # TODO: Code this section
        pass

    def save_plot_as_img(self, data_type_name):
        plot_file_path = f"{self.csv_graph_path}/{self.csv_file_name}/{data_type_name}.jpg"
        plt.savefig(plot_file_path, format="jpg")

        return plot_file_path

    def view_plots_in_explorer(self):
        if os.path.isdir(self.csv_graph_path):
            os.startfile(self.csv_graph_path)
        # TODO: Find a running instance of Windows Explorer and change dir.
        # TODO: Add support for Mac file browser.
