import os
import platform
import logging
import argparse
import shutil
import sys


def setLogging(path=None):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    if path is not None:
        file_handler = logging.FileHandler(path)
    else:
        file_handler = logging.FileHandler("sync_log.log")
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


def setParsing():
    parser = argparse.ArgumentParser("argument parser for flag usage")
    parser.add_argument('--logpath', type=str)
    parser.add_argument('--orig', type=str, help="source directory which will be synced")
    parser.add_argument('--copy', type=str, help="destination directory")
    parser.add_argument('--interval', type=str, help="synchronization interval")
    return parser


script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))


def sync_on_win(orig, dest):
    if not os.path.exists(dest):
        os.makedirs(dest)
    try:
        # folder_name = os.path.basename(orig)
        shutil.copytree(orig, dest, dirs_exist_ok=True)
    except Exception as e:
        print(f"error syncing {orig}: {e}")

    return


def sync_on_linux():
    return


def main():
    args = setParsing().parse_args()
    # logger = setLogging()
    if not args.logpath:
        logger = setLogging()
        logger.info("logging to script home location")
    else:
        logger = setLogging(args.logpath)
        logger.info(f"logging to {args.logpath}")
    if platform.system() == "Windows":
        if not args.orig:
            logger.info("Please provide sync directory")
            return
        logger.info("starting sync on windows...")
        sync_on_win(args.orig, args.copy)
    elif platform.system() == "Linux":
        logger.info("starting sync on linux...")
        sync_on_linux()
    else:
        print("script can only be run on win/linux")
        logger.error("script can only be run on win/linux")


if __name__ == '__main__':
    main()
