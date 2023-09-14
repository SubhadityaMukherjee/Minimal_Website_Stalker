# Load a website in the background using Safari and check for a specific element

import time
import argparse
from utils import *

# Create argparse to choose frequency of checking
parser = argparse.ArgumentParser(description="Check websites for changes")
parser.add_argument(
    "--t",
    type=int,
    default=15,
    help="Frequency to check websites in minutes (default: 15)",
)
args = parser.parse_args()

if __name__ == "__main__":
    # Run the main function every args.frequency minutes
    while True:
        main()
        time.sleep(args.t * 60)