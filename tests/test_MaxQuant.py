from pathlib import Path
import subprocess
from unittest.mock import MagicMock, ANY

import click
from click.testing import CliRunner
import pytest

from maxquanttools import MaxQuant as mq


@pytest.fixture
def mock_testclass():
    run = subprocess.run
    yield 
    subprocess.run = run


@pytest.fixture
def mock_env_mail(monkeypatch):
    monkeypatch.setenv('JOB_MAIL', 'christian.poitras@ircm.qc.ca')


def test_maxquant(testdir, mock_testclass):
    parameters = Path(__file__).parent.joinpath('mqpar-windows.xml')
    mail = 'christian.poitras@ircm.qc.ca'
    subprocess.run = MagicMock()
    runner = CliRunner()
    result = runner.invoke(mq.maxquant, ['-p', parameters, '--mail', mail])
    assert result.exit_code == 0
    subprocess.run.assert_any_call(['sbatch', '--cpus-per-task=2', '--mem=10G', '--mail-type=ALL', '--mail-user=' + mail, 'maxquant.sh'], check=True)


def test_maxquant_parameters(testdir, mock_testclass):
    parameters = Path(__file__).parent.joinpath('mqpar-windows.xml')
    mail = 'christian.poitras@ircm.qc.ca'
    subprocess.run = MagicMock()
    runner = CliRunner()
    result = runner.invoke(mq.maxquant, ['-p', parameters, '-c', '1', '-m', '7', '--mail', mail])
    assert result.exit_code == 0
    subprocess.run.assert_any_call(['sbatch', '--cpus-per-task=1', '--mem=7G', '--mail-type=ALL', '--mail-user=' + mail, 'maxquant.sh'], check=True)


def test_maxquant_minimum_memory(testdir, mock_testclass):
    parameters = Path(__file__).parent.joinpath('mqpar-windows.xml')
    mail = 'christian.poitras@ircm.qc.ca'
    subprocess.run = MagicMock()
    runner = CliRunner()
    result = runner.invoke(mq.maxquant, ['-p', parameters, '-m', '2', '--mail', mail])
    assert result.exit_code == 0
    subprocess.run.assert_any_call(['sbatch', '--cpus-per-task=2', '--mem=6G', '--mail-type=ALL', '--mail-user=' + mail, 'maxquant.sh'], check=True)


def test_maxquant_mailenv(testdir, mock_testclass, mock_env_mail):
    parameters = Path(__file__).parent.joinpath('mqpar-windows.xml')
    subprocess.run = MagicMock()
    runner = CliRunner()
    result = runner.invoke(mq.maxquant, ['-p', parameters, '-m', '2'])
    assert result.exit_code == 0
    subprocess.run.assert_any_call(['sbatch', '--cpus-per-task=2', '--mem=6G', '--mail-type=ALL', '--mail-user=christian.poitras@ircm.qc.ca', 'maxquant.sh'], check=True)


def test_maxquant_mailenvandparameter(testdir, mock_testclass, mock_env_mail):
    parameters = Path(__file__).parent.joinpath('mqpar-windows.xml')
    mail = 'test@ircm.qc.ca'
    subprocess.run = MagicMock()
    runner = CliRunner()
    result = runner.invoke(mq.maxquant, ['-p', parameters, '-m', '2', '--mail', mail])
    assert result.exit_code == 0
    subprocess.run.assert_any_call(['sbatch', '--cpus-per-task=2', '--mem=6G', '--mail-type=ALL', '--mail-user=' + mail, 'maxquant.sh'], check=True)
