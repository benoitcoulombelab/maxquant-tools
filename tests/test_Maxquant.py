import os
import subprocess
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from click.testing import CliRunner

from maxquanttools import Maxquant, FixParameters


@pytest.fixture
def mock_testclass():
    fixparameters = FixParameters.fixparameters_
    run = subprocess.run
    yield
    subprocess.run = run
    FixParameters.fixparameters_ = fixparameters


@pytest.fixture
def mock_env_mail(monkeypatch):
    monkeypatch.setenv('JOB_MAIL', 'christian.poitras@ircm.qc.ca')


def test_maxquant(pytester, mock_testclass):
    parameters = Path(__file__).parent.joinpath('mqpar-windows.xml')
    mail = 'christian.poitras@ircm.qc.ca'
    output = 'mqpar-run.xml'
    FixParameters.fixparameters_ = MagicMock()
    subprocess.run = MagicMock()
    runner = CliRunner()
    result = runner.invoke(Maxquant.maxquant, ['--parameters', parameters, '--mail', mail])
    assert result.exit_code == 0
    FixParameters.fixparameters_.assert_any_call(parameters, rawdir=os.getcwd(), threads=2, output='mqpar-run.xml')
    subprocess.run.assert_any_call(
        ['sbatch', '--cpus-per-task=2', '--mem=10G', '--mail-type=ALL', '--mail-user=' + mail, 'maxquantcmd-mono.sh',
         str(output)],
        check=True)


def test_maxquant_parameters(pytester, mock_testclass):
    parameters = Path(__file__).parent.joinpath('mqpar-windows.xml')
    mail = 'christian.poitras@ircm.qc.ca'
    rawdir = 'raws'
    output = 'mqpar-testout.xml'
    FixParameters.fixparameters_ = MagicMock()
    subprocess.run = MagicMock()
    runner = CliRunner()
    result = runner.invoke(Maxquant.maxquant,
                           ['--parameters', parameters, '--rawdir', rawdir, '--max-threads', '1', '--max-mem', '7',
                            '--mail', mail, '--parameters-output', output, '-p', '18', '-e', '20'])
    assert result.exit_code == 0
    FixParameters.fixparameters_.assert_any_call(parameters, rawdir=rawdir, threads=1, output=output)
    subprocess.run.assert_any_call(
        ['sbatch', '--cpus-per-task=1', '--mem=7G', '--mail-type=ALL', '--mail-user=' + mail, 'maxquantcmd-mono.sh',
         '-p', '18', '-e', '20',
         str(output)],
        check=True)


def test_maxquant_dryrun(pytester, mock_testclass):
    parameters = Path(__file__).parent.joinpath('mqpar-windows.xml')
    mail = 'christian.poitras@ircm.qc.ca'
    output = 'mqpar-run.xml'
    FixParameters.fixparameters_ = MagicMock()
    subprocess.run = MagicMock()
    runner = CliRunner()
    result = runner.invoke(Maxquant.maxquant, ['--parameters', parameters, '--mail', mail, '-n'])
    assert result.exit_code == 0
    FixParameters.fixparameters_.assert_any_call(parameters, rawdir=os.getcwd(), threads=2, output='mqpar-run.xml')
    subprocess.run.assert_any_call(
        ['maxquantcmd-mono.sh', '-n', str(output)],
        check=True)


def test_maxquant_minimum_memory(pytester, mock_testclass):
    parameters = Path(__file__).parent.joinpath('mqpar-windows.xml')
    mail = 'christian.poitras@ircm.qc.ca'
    output = 'mqpar-run.xml'
    FixParameters.fixparameters_ = MagicMock()
    subprocess.run = MagicMock()
    runner = CliRunner()
    result = runner.invoke(Maxquant.maxquant, ['--parameters', parameters, '--max-mem', '2', '--mail', mail])
    assert result.exit_code == 0
    FixParameters.fixparameters_.assert_any_call(parameters, rawdir=os.getcwd(), threads=2, output='mqpar-run.xml')
    subprocess.run.assert_any_call(
        ['sbatch', '--cpus-per-task=2', '--mem=6G', '--mail-type=ALL', '--mail-user=' + mail, 'maxquantcmd-mono.sh',
         str(output)],
        check=True)


def test_maxquant_mailenv(pytester, mock_testclass, mock_env_mail):
    parameters = Path(__file__).parent.joinpath('mqpar-windows.xml')
    output = 'mqpar-run.xml'
    FixParameters.fixparameters_ = MagicMock()
    subprocess.run = MagicMock()
    runner = CliRunner()
    result = runner.invoke(Maxquant.maxquant, ['--parameters', parameters])
    assert result.exit_code == 0
    FixParameters.fixparameters_.assert_any_call(parameters, rawdir=os.getcwd(), threads=2, output='mqpar-run.xml')
    subprocess.run.assert_any_call(
        ['sbatch', '--cpus-per-task=2', '--mem=10G', '--mail-type=ALL', '--mail-user=christian.poitras@ircm.qc.ca',
         'maxquantcmd-mono.sh', str(output)], check=True)


def test_maxquant_mailenvandparameter(pytester, mock_testclass, mock_env_mail):
    parameters = Path(__file__).parent.joinpath('mqpar-windows.xml')
    mail = 'test@ircm.qc.ca'
    output = 'mqpar-run.xml'
    FixParameters.fixparameters_ = MagicMock()
    subprocess.run = MagicMock()
    runner = CliRunner()
    result = runner.invoke(Maxquant.maxquant, ['--parameters', parameters, '--mail', mail])
    assert result.exit_code == 0
    FixParameters.fixparameters_.assert_any_call(parameters, rawdir=os.getcwd(), threads=2, output='mqpar-run.xml')
    subprocess.run.assert_any_call(
        ['sbatch', '--cpus-per-task=2', '--mem=10G', '--mail-type=ALL', '--mail-user=' + mail, 'maxquantcmd-mono.sh',
         str(output)],
        check=True)
