import glob
import argparse
import os

import pandas as pd
import seaborn as sns
import yaml
from matplotlib import pyplot as plt

if __name__ == "__main__":
    if not os.path.exists("./plots"):
        os.makedirs("./plots")

    # load in the settings
    config = yaml.load(open("./config.yaml", "r"), Loader=yaml.FullLoader)
    config = argparse.Namespace(**config)

    # set seaborn style
    sns.set_style("darkgrid")
    color_palette = sns.color_palette("colorblind")

    # extract the filename, or all filenames
    targets = []
    if config.data_target is None:
        all_paths = glob.glob("./raw_data/*.csv")
        for path in all_paths:
            targets.append(os.path.basename(path))
    else:
        targets.append(config.data_target)

    for target in targets:
        # we save the target plot in this folder
        save_dir = os.path.join("./plots", target.split(".")[0])
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # read in the data
        dataframe = pd.read_csv(os.path.join("./raw_data", target))

        # plot the big plot
        ax = sns.boxplot(dataframe, showfliers=False, whis=99999, palette=color_palette)
        ax.set(xlabel=config.xlabel, ylabel=config.ylabel, title=config.title)
        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, f"all_plots.{config.save_format}"), dpi=config.dpi)
        plt.close()

        # plot everything individually
        for i, header in enumerate(dataframe):
            # generate the box plot
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
                os.path.join(save_dir, f"{header}.{config.save_format}"), dpi=config.dpi
            )
            plt.close()
