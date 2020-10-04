import requests
import pathlib
import pandas as pd
import time
import random
import argparse

import mod_info
import check_n_download




if __name__ == "__main__":
    argparser = argparse.ArgumentParser("mod updater",description=
    """
    Commandline tool to update mods in FS19.
    """,epilog=
    """
    There is no guarantee that this will work when you use it, please don't be mad.
    """
    )
    argparser.add_argument("-f", "--mod-dir", type=pathlib.Path, required=True,help=
    """
    Path to mod-directory (usually "HOME/my games/FarmingSimulator2019/mods/")
    """)

    args = argparser.parse_args()
    mod_path: pathlib.Path = args.mod_dir
    
    available_mods = mod_info.fetch_all_mod_info()

    installed_mods = check_n_download.check_local_mods(mod_path)
    
    merged = installed_mods.merge(available_mods,how="left",on=["mod_title","author"])

    merged['duplicate_entries'] = merged.duplicated(subset=['mod_title','author'],keep=False)
    
    print("duplicated entries")
    print(merged.loc[merged.duplicate_entries])
    print("unable to match following")
    print(merged.loc[merged.mod_id.isna()])
    #remove problematic mods..
    merged = merged.loc[~merged.duplicate_entries]
    merged = merged.loc[merged.mod_id.notna()]

    #del merged['duplicate_entries']
    check_n_download.check_and_update(merged,mod_path)

    print("done")