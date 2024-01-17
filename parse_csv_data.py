import pandas
import matplotlib.pyplot as plt
import seaborn as sns


class ParseCsvData:
    def __init__(self, csv_file_path):
        print(csv_file_path)
        self.df = pandas.read_csv(csv_file_path)
        print(self.df)
        self.df_dict = self.df.to_dict()

        self.test_data()

    def test_data(self):
        bar_colors = ["tab:green", "tab:red"]
        asset_state = ["Pass", "Fail"]
        num_pass = self.df[self.df.Reason == "Pass"].shape[0]
        num_fail = self.df.shape[0] - num_pass
        state_count = [num_pass, num_fail]

        fig, ax = plt.subplots()
        bar_values = ax.bar(asset_state, state_count)
        ax.bar(asset_state, state_count, color=bar_colors)
        # sns.barplot(x=asset_state, y=state_count, hue=asset_state, legend=False, palette=bar_colors)
        ax.grid(axis="y")
        ax.set(ylabel="Asset Count", xlabel="Asset State", axisbelow=True)
        ax.bar_label(bar_values)

        plt.title("Asset Pass/Fail State")
        plt.show()
