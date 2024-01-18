import argparse
from enum import Enum
from typing import TypedDict
import json

# API functions
def deeplabcut(args: dict):
    # only import code that depends on deeplabcut if we're actually going to use it
    from dlc_runner import run_deeplabcut

    config_path: str = args['config_path']
    videos: list[str] = args['videos']

    run_deeplabcut(config_path, videos)

class Extraction(TypedDict):
    name: str
    ftir_path: str
    tracking_path: str
    dest_path: str

def features(args: dict):
    from process import extract_features

    extractions: list[Extraction] = args['extractions']

    for extraction in extractions:
        extract_features(
            extraction['name'],
            extraction['ftir_path'],
            extraction['tracking_path'],
            extraction['dest_path']
        )

def summary(args: dict):
    from summary import generate_summary_csv

    features_dir: str = args['features_dir']
    summary_path: str = args['summary_path']

    generate_summary_csv(features_dir, summary_path)

# Palmreader <-> Analysis API
# The following code is relied upon by the Palmreader software. Take special care when modifying it.
class ApiFunction(Enum):
    DEEPLABCUT = 'deeplabcut'
    FEATURES = 'features'
    SUMMARY = 'summary'

    def __str__(self):
        return self.value

def main():
    p = argparse.ArgumentParser()

    # the function to call, one of the ApiFunction variants
    p.add_argument('--function', type=ApiFunction, choices=list(ApiFunction), required=True, dest='function')
    # a JSON literal that will be parsed into function arguments for the given function
    # the structure of this literal depends on the function being called
    p.add_argument('--args', type=str, required=True, dest='args')

    args = p.parse_args()

    api_args = json.loads(args.args)
    if args.function == ApiFunction.DEEPLABCUT:
        deeplabcut(api_args)
    elif args.function == ApiFunction.FEATURES:
        features(api_args)
    elif args.function == ApiFunction.SUMMARY:
        summary(api_args)

if __name__ == '__main__':
    main()
