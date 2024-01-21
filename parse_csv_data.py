import pandas, os
import matplotlib.pyplot as plt
import seaborn as sns


class ParseCsvData:
    def __init__(self, csv_file_path):
        self.x_axis_data = []
        self.x_axis_label = []
        self.data_type_name = ""

        self.csv_dir_path = f"{csv_file_path.rpartition('/')[0]}/Graphs"
        self.csv_file_name = csv_file_path.rpartition("/")[2].replace(".csv", "")

        self.df = pandas.read_csv(csv_file_path)

        # Report Types - Pass:Fail ratio by date (line plot),  severity reason (pie chart)
        self.get_pass_state_report()
        self.get_severity_report()
        self.get_severity_reason_report()
        self.view_plots_in_explorer()

    def get_pass_state_report(self):
        pass

    def get_severity_report(self):
        """
        Loop through the dataframe rows and increment specific list index pertaining to the level of severity.
        This will create data to show how many of each severity type was found.
        :return: None
        """
        self.data_type_name = "Severity"
        self.x_axis_data = [0, 0, 0, 0]

        for index, row in self.df.iterrows():
            if row["Severity"] == "Critical":
                self.x_axis_data[0] += 1
            elif row["Severity"] == "High":
                self.x_axis_data[1] += 1
            elif row["Severity"] == "Medium":
                self.x_axis_data[2] += 1
            elif row["Severity"] == "Low":
                self.x_axis_data[3] += 1

        self.x_axis_label = ["Critical", "High", "Medium", "Low"]

        self.plot_data()

    def get_severity_reason_report(self):
        pass

    def plot_data(self):
        """
        Called by data functions.  Configures and generates the visual plot then shows it to the user and
        saves it as a jpg file in the same directory as the source csv files.
        :param:
        :return:
        """
        bar_colors = ["#FF0000", "#FFA500", "#FFFF00", "#00FF00"]

        fig, ax = plt.subplots()
        bar_values = ax.bar(self.x_axis_label, self.x_axis_data)
        sns.barplot(x=self.x_axis_label, y=self.x_axis_data, hue=self.x_axis_label, legend=False, palette=bar_colors)
        ax.grid(axis="y")
        ax.set(ylabel=f"{ self.data_type_name} Count", xlabel=f"{ self.data_type_name} Type", axisbelow=True)
        ax.bar_label(bar_values)

        plt.title(f"Asset {self.data_type_name} Count")
        plot_file_name = f"{self.csv_dir_path}/{self.csv_file_name}_{self.data_type_name}.jpg"
        print(plot_file_name)
        plt.savefig(plot_file_name, format="jpg")

        self.reset_variables()

    def reset_variables(self):
        """
        Reset variables to be reused with other data
        :return: None
        """
        self.x_axis_data = []
        self.x_axis_label = []
        self.data_type_name = ""

    def view_plots_in_explorer(self):
        os.startfile(self.csv_dir_path)
