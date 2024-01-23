import os, helper
import matplotlib.pyplot as plt


class GenerateGraphs:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.csv_graph_path = helper.get_graph_path(self.csv_file_path)
        self.csv_file_name = helper.get_capture_type(self.csv_file_path)

        # Verify that a Graph subdirectory exists under the current date directory.
        helper.directory_exists(f"{self.csv_graph_path}/{self.csv_file_name}")

        # self.view_plots_in_explorer()

    def make_bar_plot(self, *args):
        """
        Called by generate_graph_data to make a bar plot.
        :param args: data_type_name, plot_labels, plot_data, bar_colors
        :return: None
        """

        fig, ax = plt.subplots()
        plt.title(f"Asset {args[0]} Count")
        # Set the data value within the bar container
        bar_values = ax.bar(args[1], args[2])
        ax.bar_label(bar_values, label_type="center")
        ax.bar(x=args[1], height=args[2], color=args[3])
        # Create the horizontal grid lines and set them behind the bar containers
        ax.grid(axis="y")
        ax.set(ylabel=f"{args[0]} Count", xlabel=f"{args[0]} Type", axisbelow=True)

        plot_file_path = self.save_plot_as_img(args[0])

        # Clear the plot axis and figure to prepare for the next plot generation
        plt.cla()
        plt.clf()
        return plot_file_path

    def make_pie_chart(self, *args):
        """
        Makes a pie chart
        :param args: data_type_name, plot_labels, plot_data, bar_colors
        :return: None
        """
        fig, ax = plt.subplots()
        plt.title(args[0])
        ax.pie(args[2], labels=args[1], colors=args[3], autopct="%1.1f%%")

        plot_file_path = self.save_plot_as_img(args[0])

        # Clear the plot axis and figure to prepare for the next plot generation
        plt.cla()
        plt.clf()
        return plot_file_path

    def save_plot_as_img(self, data_type_name):
        plot_file_path = f"{self.csv_graph_path}/{self.csv_file_name}/{data_type_name}.jpg"
        plt.savefig(plot_file_path, format="jpg")

        return plot_file_path

    def view_plots_in_explorer(self):
        if os.path.isdir(self.csv_graph_path):
            os.startfile(self.csv_graph_path)
        # TODO: Find a running instance of Windows Explorer and change dir.
        # TODO: Add support for Mac file browser.
