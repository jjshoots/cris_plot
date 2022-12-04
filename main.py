import argparse
import os.path as path

import pandas as pd
import seaborn as sns
import yaml
from matplotlib import pyplot as plt

SAVE_DIR = "./plots"

if __name__ == "__main__":
    # load in the settings
    config = yaml.load(open("./config.yaml", "r"), Loader=yaml.FullLoader)
    config = argparse.Namespace(**config)

    # read in the data
    dataframe = pd.read_csv(config.data_target)

    # set seaborn style
    sns.set_style("darkgrid")
    color_palette = sns.color_palette("colorblind")

    # plot the big plot
    ax = sns.boxplot(dataframe, showfliers=False, whis=99999, palette=color_palette)
    ax.set(xlabel=config.xlabel, ylabel=config.ylabel, title=config.title)
    plt.tight_layout()
    plt.savefig(path.join(SAVE_DIR, f"all_plots.{config.save_format}"), dpi=config.dpi)
    plt.close()

    # plot everything individually
    for i, header in enumerate(dataframe):
        ax = sns.boxplot(
            dataframe[
                [
                    header,
                ]
            ],
            showfliers=False,
            whis=99999,
            palette=color_palette[i:],

        )
        ax.set(xlabel=config.xlabel, ylabel=config.ylabel, title=config.title)
        plt.tight_layout()
        plt.savefig(
            path.join(SAVE_DIR, f"{header}.{config.save_format}"), dpi=config.dpi
        )
        plt.close()
