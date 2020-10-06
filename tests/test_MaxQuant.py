from pathlib import Path
import subprocess
from unittest.mock import MagicMock, ANY

import click
from click.testing import CliRunner
import pytest

from maxquantparameters import MaxQuant as mq


@pytest.fixture
def mock_testclass():
    run = subprocess.run
    yield 
    subprocess.run = run


def test_maxquant(testdir, mock_testclass):
    parameters = Path(__file__).parent.joinpath('mqpar-windows.xml')
    subprocess.run = MagicMock()
    runner = CliRunner()
    result = runner.invoke(mq.maxquant, ['-p', parameters])
    assert result.exit_code == 0
    subprocess.run.assert_any_call(['sbatch', '--cpus-per-task=2', '--mem=10G', 'maxquant.sh'], check=True)


def test_maxquant_parameters(testdir, mock_testclass):
    parameters = Path(__file__).parent.joinpath('mqpar-windows.xml')
    subprocess.run = MagicMock()
    runner = CliRunner()
    result = runner.invoke(mq.maxquant, ['-p', parameters, '-c', '1', '-m', '7'])
    assert result.exit_code == 0
    subprocess.run.assert_any_call(['sbatch', '--cpus-per-task=1', '--mem=7G', 'maxquant.sh'], check=True)


def test_maxquant_minimum_memory(testdir, mock_testclass):
    parameters = Path(__file__).parent.joinpath('mqpar-windows.xml')
    subprocess.run = MagicMock()
    runner = CliRunner()
    result = runner.invoke(mq.maxquant, ['-p', parameters, '-m', '2'])
    assert result.exit_code == 0
    subprocess.run.assert_any_call(['sbatch', '--cpus-per-task=2', '--mem=6G', 'maxquant.sh'], check=True)
