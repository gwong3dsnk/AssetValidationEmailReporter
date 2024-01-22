import json, pandas, os
import generate_graphs, email_report


class GenerateGraphData:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.x_axis_data = []
        self.y_axis_data = []
        self.data_type_name = ""
        self.plot_file_paths = []

        self.df = pandas.read_csv(csv_file_path)
        self.gg = generate_graphs.GenerateGraphs(csv_file_path)

    def generate_reports(self):
        self.get_severity_report()
        self.get_fail_reason_report()
        return self.plot_file_paths

    # def get_pass_state_report(self):
    #     self.data_type_name = "Pass/Fail State"
    #
    #     self.x_axis_label = [dir_name for dir_name in os.listdir(self.csv_file_path)
    #                          if os.path.isdir(f"{self.csv_file_path}/{dir_name}")]
    #
    #     num_pass = self.df[self.df.Reason == "Pass"].shape[0]
    #     num_fail = self.df.shape[0] - num_pass
    #     self.x_axis_data = [num_pass, num_fail]

    def get_severity_report(self):
        """
        Loop through the dataframe rows and increment specific list index pertaining to the level of severity.
        This will create data to show how many of each severity type was found.
        :return: None
        """
        self.data_type_name = "Severity"
        self.y_axis_data = [0, 0, 0, 0]
        self.x_axis_data = ["Critical", "High", "Medium", "Low"]
        bar_colors = ["#FF0000", "#FFA500", "#FFFF00", "#00FF00"]

        for index, row in self.df.iterrows():
            if row["Severity"] == "Critical":
                self.y_axis_data[0] += 1
            elif row["Severity"] == "High":
                self.y_axis_data[1] += 1
            elif row["Severity"] == "Medium":
                self.y_axis_data[2] += 1
            elif row["Severity"] == "Low":
                self.y_axis_data[3] += 1

        plot_file_path = self.gg.make_bar_plot(
            self.data_type_name, self.x_axis_data, self.y_axis_data, bar_colors
        )
        self.plot_file_paths.append(plot_file_path)
        self.reset_variables()

    def get_fail_reason_report(self):
        self.data_type_name = "FailReasons"
        self.y_axis_data = [0, 0, 0, 0, 0, 0]
        self.x_axis_data = ["TriangleCount", "LODCount", "MatCount", "InvalidNaniteMat", "DevAsset", "NeverStream"]
        bar_colors = ["#362925", "#74482a", "#855832", "a17e61", "#dbc9b8", "#F9F6EE"]

        reason_data = [row["FailReasons"] for index, row in self.df.iterrows() if row["Severity"] != "None;"]

        reason_text = []
        for data in reason_data:
            reason = data.split(";")
            for item in reason:
                if item != "":
                    reason_text.append(item)

        # Go through reason_text and create a dictionary where the keys are the reasons and values are the count of
        # occurrences
        reason_dict = {item: reason_text.count(item) for item in reason_text}

        # Increment the y_axis_data elements based on reason occurrences.
        for key, value in reason_dict.items():
            for x_data in self.x_axis_data:
                if key == x_data:
                    idx = self.x_axis_data.index(x_data)
                    self.y_axis_data[idx] = self.y_axis_data[idx] + value

        plot_file_path = self.gg.make_pie_chart(
            self.data_type_name, self.x_axis_data, self.y_axis_data, bar_colors
        )
        self.plot_file_paths.append(plot_file_path)
        self.reset_variables()

    def reset_variables(self):
        """
        Reset variables to be reused with other data
        :return: None
        """
        self.x_axis_data = []
        self.y_axis_data = []
        self.data_type_name = ""
