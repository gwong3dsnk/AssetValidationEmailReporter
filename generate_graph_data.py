import pandas, generate_graphs


class GenerateGraphData:
    def __init__(self):
        self.plot_labels = []
        self.plot_data = []
        self.data_type_name = ""
        self.plot_file_paths = []
        self.paths_per_csv = []

    def generate_reports(self, path):
        df = pandas.read_csv(path)
        gg = generate_graphs.GenerateGraphs(path)

        self.get_severity_report(df, gg)
        self.get_fail_reason_report(df, gg)
        full_line_report = self.generate_asset_report_list(df)

        self.paths_per_csv.append(self.plot_file_paths)
        self.plot_file_paths = []

        return self.paths_per_csv, full_line_report

    def get_severity_report(self, df, gg):
        """
        Loop through the dataframe rows and increment specific list index pertaining to the level of severity.
        This will create data to show how many of each severity type was found.
        :return: None
        """
        self.data_type_name = "Severity"
        self.plot_data = [0, 0, 0, 0]
        self.plot_labels = ["Critical", "High", "Medium", "Low"]
        bar_colors = ["#FF0000", "#FFA500", "#FFFF00", "#00FF00"]

        for index, row in df.iterrows():
            if row["Severity"] == "Critical":
                self.plot_data[0] += 1
            elif row["Severity"] == "High":
                self.plot_data[1] += 1
            elif row["Severity"] == "Medium":
                self.plot_data[2] += 1
            elif row["Severity"] == "Low":
                self.plot_data[3] += 1

        plot_file_path = gg.make_bar_plot(
            self.data_type_name, self.plot_labels, self.plot_data, bar_colors
        )
        self.plot_file_paths.append(plot_file_path)
        self.reset_variables()

    def get_fail_reason_report(self, df, gg):
        """
        Generate a pie chart that shows the percentages that each fail reason makes up.
        :param df:
        :param gg:
        :return:
        """
        self.data_type_name = "All_Fail_Reasons"
        self.plot_data = [0, 0, 0, 0, 0, 0]
        self.plot_labels = ["TriangleCount", "LODCount", "MatCount", "InvalidNaniteMat", "DevAsset", "NeverStream"]
        bar_colors = ["#78281F", "#B03A2E", "#E74C3C", "#F1948A", "#FADBD8", "#F9F6EE"]

        reason_data = [row["FailReasons"] for index, row in df.iterrows() if row["Severity"] != "None;"]

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
            for x_data in self.plot_labels:
                if key == x_data:
                    idx = self.plot_labels.index(x_data)
                    self.plot_data[idx] = self.plot_data[idx] + value

        # Clean out list elements where the data is 0 as having it will cause label text overlap in the plot.
        idx_to_remove = []
        for n in range(0, len(self.plot_data)):
            if self.plot_data[n] == 0:
                idx_to_remove.append(n)
            n += 1
        idx_to_remove.reverse()  # Reverse list so we start removing list elements from the end first.
        for idx in idx_to_remove:
            self.plot_data.pop(idx)
            self.plot_labels.pop(idx)

        plot_file_path = gg.make_pie_chart(
            self.data_type_name, self.plot_labels, self.plot_data, bar_colors
        )
        self.plot_file_paths.append(plot_file_path)
        self.reset_variables()

    def generate_asset_report_list(self, df):
        asset_path_data = []
        severity_levels = ["Critical", "High", "Medium"]
        full_line_report = []

        for n in range(0, len(severity_levels)):
            report = []
            reasons = [row["FailReasons"] for index, row in df.iterrows() if row["Severity"] == severity_levels[n]]
            asset_names = [row["AssetName"] for index, row in df.iterrows() if row["Severity"] == severity_levels[n]]
            asset_paths = [row["ObjectPath"] for index, row in df.iterrows() if row["Severity"] == severity_levels[n]]

            for path in asset_paths:
                new_path = path.rpartition("/")[0]
                asset_path_data.append(new_path)

            for i in range(0, len(reasons)):
                report_line = f"{asset_names[i]} --> {reasons[i]} --> {asset_path_data[i]}"
                report.append(report_line)

            full_line_report.append(report)

        return full_line_report

    def reset_variables(self):
        """
        Reset variables to be reused with other data
        :return: None
        """
        self.plot_labels = []
        self.plot_data = []
        self.data_type_name = ""
