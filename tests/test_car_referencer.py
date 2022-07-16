#!/usr/bin/env python

"""Tests for `car_referencer` package."""

import glob
import os
import subprocess

import pandas as pd
import pytest
import xarray as xr

import car_referencer.index as idx
from car_referencer import car_referencer


def create_test_zarr(tmp_path):
    xr.tutorial.load_dataset("air_temperature").chunk(
        {"time": 100, "lat": 5, "lon": 5}
    ).to_zarr(str(tmp_path) + "/example.zarr")


@pytest.fixture
def test_cars(tmp_path):
    create_test_zarr(tmp_path)
    with open(f"{str(tmp_path)}/old-example.json", "w") as f:
        f.write("{}")
    if os.environ.get("GOPATH"):
        gopath = os.environ["GOPATH"] + "/go/bin"
    else:
        gopath = os.environ["HOME"] + "/go/bin"
    assert os.path.exists(gopath + "/linux2ipfs"), "linux2ipfs could not be found"
    subprocess.check_output(
        f"{gopath}/linux2ipfs -car-size 3382286 -driver car-{str(tmp_path)}/example.%d.car -incremental-file {str(tmp_path)}/old-example.json {str(tmp_path)}/example.zarr",
        shell=True,
    )
    return sorted(glob.glob(f"{str(tmp_path)}/example.*.car"))


@pytest.fixture


def test_index_creation(test_cars):
    print(test_cars)
    index = idx.generate_index(test_cars)
    assert index is not None
    assert isinstance(index, pd.DataFrame)


def test_preffs_creation():
    pass
