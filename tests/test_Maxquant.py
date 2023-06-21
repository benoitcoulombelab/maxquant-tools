import logging
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


@pytest.fixture
def mock_env_maxquant_module(monkeypatch):
    monkeypatch.setenv('MAXQUANT', 'maxquant')
    monkeypatch.setenv('MAXQUANT_VERSION', '2.0.1.0')


@pytest.fixture
def beluga(monkeypatch):
    monkeypatch.setenv('CC_CLUSTER', 'beluga')


def test_maxquant(pytester, mock_testclass):
    parameters = Path(__file__).parent.joinpath('mqpar-windows.xml')
    mail = 'christian.poitras@ircm.qc.ca'
    output = 'mqpar-run.xml'
    FixParameters.fixparameters_ = MagicMock()
    subprocess.run = MagicMock()
    runner = CliRunner()
    result = runner.invoke(Maxquant.maxquant, ['--parameters', parameters, '--mail', mail])
    assert result.exit_code == 0
    FixParameters.fixparameters_.assert_any_call(parameters, rawdir=os.getcwd(), threads=24, output='mqpar-run.xml')
    subprocess.run.assert_any_call(
        ['sbatch', '--cpus-per-task=24', '--mem=120G', '--mail-type=END,FAIL', '--mail-user=' + mail,
         'maxquantcmd-mono.sh',
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
                           ['--parameters', parameters, '--rawdir', rawdir,
                            '--mail', mail, '--parameters-output', output, '-p', '18', '-e', '20'])
    assert result.exit_code == 0
    FixParameters.fixparameters_.assert_any_call(parameters, rawdir=rawdir, threads=24, output=output)
    subprocess.run.assert_any_call(
        ['sbatch', '--cpus-per-task=24', '--mem=120G', '--mail-type=END,FAIL', '--mail-user=' + mail,
         'maxquantcmd-mono.sh',
         '-p', '18', '-e', '20',
         str(output)],
        check=True)


def test_maxquant_ignoremail(pytester, mock_testclass):
    parameters = Path(__file__).parent.joinpath('mqpar-windows.xml')
    output = 'mqpar-run.xml'
    FixParameters.fixparameters_ = MagicMock()
    subprocess.run = MagicMock()
    runner = CliRunner()
    result = runner.invoke(Maxquant.maxquant,
                           ['--parameters', parameters, '--ignore-mail'])
    assert result.exit_code == 0
    FixParameters.fixparameters_.assert_any_call(parameters, rawdir=os.getcwd(), threads=24, output='mqpar-run.xml')
    subprocess.run.assert_any_call(
        ['sbatch', '--cpus-per-task=24', '--mem=120G', 'maxquantcmd-mono.sh',
         str(output)],
        check=True)


def test_maxquant_beluga(pytester, mock_testclass, beluga):
    parameters = Path(__file__).parent.joinpath('mqpar-windows.xml')
    mail = 'christian.poitras@ircm.qc.ca'
    output = 'mqpar-run.xml'
    FixParameters.fixparameters_ = MagicMock()
    subprocess.run = MagicMock()
    runner = CliRunner()
    result = runner.invoke(Maxquant.maxquant, ['--parameters', parameters, '--mail', mail])
    assert result.exit_code == 0
    FixParameters.fixparameters_.assert_any_call(parameters, rawdir=os.getcwd(), threads=40, output='mqpar-run.xml')
    subprocess.run.assert_any_call(
        ['sbatch', '--cpus-per-task=40', '--mem=180G', '--mail-type=END,FAIL', '--mail-user=' + mail,
         'maxquantcmd-mono.sh',
         str(output)],
        check=True)


def test_maxquant_config(pytester, mock_testclass):
    parameters = Path(__file__).parent.joinpath('mqpar-windows.xml')
    mail = 'christian.poitras@ircm.qc.ca'
    output = 'mqpar-run.xml'
    config = 'maxquant.yml'
    with open(config, 'w') as outfile:
        outfile.write('threads: 48\n')
        outfile.write('memory: 185')
    FixParameters.fixparameters_ = MagicMock()
    subprocess.run = MagicMock()
    runner = CliRunner()
    result = runner.invoke(Maxquant.maxquant, ['--parameters', parameters, '--mail', mail])
    assert result.exit_code == 0
    FixParameters.fixparameters_.assert_any_call(parameters, rawdir=os.getcwd(), threads=48, output='mqpar-run.xml')
    subprocess.run.assert_any_call(
        ['sbatch', '--cpus-per-task=48', '--mem=185G', '--mail-type=END,FAIL', '--mail-user=' + mail,
         'maxquantcmd-mono.sh',
         str(output)],
        check=True)


def test_maxquant_belugaandconfig(pytester, mock_testclass, beluga):
    parameters = Path(__file__).parent.joinpath('mqpar-windows.xml')
    mail = 'christian.poitras@ircm.qc.ca'
    output = 'mqpar-run.xml'
    config = 'maxquant.yml'
    with open(config, 'w') as outfile:
        outfile.write('threads: 48\n')
        outfile.write('memory: 185')
    FixParameters.fixparameters_ = MagicMock()
    subprocess.run = MagicMock()
    runner = CliRunner()
    result = runner.invoke(Maxquant.maxquant, ['--parameters', parameters, '--mail', mail])
    assert result.exit_code == 0
    FixParameters.fixparameters_.assert_any_call(parameters, rawdir=os.getcwd(), threads=48, output='mqpar-run.xml')
    subprocess.run.assert_any_call(
        ['sbatch', '--cpus-per-task=48', '--mem=185G', '--mail-type=END,FAIL', '--mail-user=' + mail,
         'maxquantcmd-mono.sh',
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
    FixParameters.fixparameters_.assert_any_call(parameters, rawdir=os.getcwd(), threads=24, output='mqpar-run.xml')
    subprocess.run.assert_any_call(
        ['maxquantcmd-mono.sh', '-n', str(output)],
        check=True)


def test_maxquant_minimum_memory(pytester, mock_testclass):
    parameters = Path(__file__).parent.joinpath('mqpar-windows.xml')
    mail = 'christian.poitras@ircm.qc.ca'
    output = 'mqpar-run.xml'
    config = 'maxquant.yml'
    with open(config, 'w') as outfile:
        outfile.write('threads: 1\n')
        outfile.write('memory: 4')
    FixParameters.fixparameters_ = MagicMock()
    subprocess.run = MagicMock()
    runner = CliRunner()
    result = runner.invoke(Maxquant.maxquant, ['--parameters', parameters, '--mail', mail])
    assert result.exit_code == 0
    FixParameters.fixparameters_.assert_any_call(parameters, rawdir=os.getcwd(), threads=1, output='mqpar-run.xml')
    subprocess.run.assert_any_call(
        ['sbatch', '--cpus-per-task=1', '--mem=6G', '--mail-type=END,FAIL', '--mail-user=' + mail,
         'maxquantcmd-mono.sh',
         str(output)],
        check=True)


def test_maxquant_minimum_threads(pytester, mock_testclass):
    parameters = Path(__file__).parent.joinpath('mqpar-windows.xml')
    mail = 'christian.poitras@ircm.qc.ca'
    output = 'mqpar-run.xml'
    config = 'maxquant.yml'
    with open(config, 'w') as outfile:
        outfile.write('threads: 0\n')
        outfile.write('memory: 60')
    FixParameters.fixparameters_ = MagicMock()
    subprocess.run = MagicMock()
    runner = CliRunner()
    result = runner.invoke(Maxquant.maxquant, ['--parameters', parameters, '--mail', mail])
    assert result.exit_code == 0
    FixParameters.fixparameters_.assert_any_call(parameters, rawdir=os.getcwd(), threads=1, output='mqpar-run.xml')
    subprocess.run.assert_any_call(
        ['sbatch', '--cpus-per-task=1', '--mem=60G', '--mail-type=END,FAIL', '--mail-user=' + mail,
         'maxquantcmd-mono.sh',
         str(output)],
        check=True)


def test_maxquant_module(pytester, mock_testclass, mock_env_maxquant_module):
    parameters = Path(__file__).parent.joinpath('mqpar-windows.xml')
    mail = 'christian.poitras@ircm.qc.ca'
    output = 'mqpar-run.xml'
    os.mkdir('maxquant')
    Path('maxquant/maxquant-2.0.1.0.sif').touch()
    logging.debug('maxquant={} and version={}'.format(os.environ.get('MAXQUANT'), os.environ.get('MAXQUANT_VERSION')))
    FixParameters.fixparameters_ = MagicMock()
    subprocess.run = MagicMock()
    runner = CliRunner()
    result = runner.invoke(Maxquant.maxquant, ['--parameters', parameters, '--mail', mail])
    assert result.exit_code == 0
    FixParameters.fixparameters_.assert_any_call(parameters, rawdir=os.getcwd(), threads=24, output='mqpar-run.xml')
    subprocess.run.assert_any_call(
        ['sbatch', '--cpus-per-task=24', '--mem=120G', '--mail-type=END,FAIL',
         '--mail-user=christian.poitras@ircm.qc.ca',
         'maxquantcmd-apptainer.sh', str(output)], check=True)


def test_maxquant_module_nocontainer(pytester, mock_testclass, mock_env_maxquant_module):
    parameters = Path(__file__).parent.joinpath('mqpar-windows.xml')
    mail = 'christian.poitras@ircm.qc.ca'
    output = 'mqpar-run.xml'
    logging.debug('maxquant={} and version={}'.format(os.environ.get('MAXQUANT'), os.environ.get('MAXQUANT_VERSION')))
    FixParameters.fixparameters_ = MagicMock()
    subprocess.run = MagicMock()
    runner = CliRunner()
    result = runner.invoke(Maxquant.maxquant, ['--parameters', parameters, '--mail', mail])
    assert result.exit_code == 0
    FixParameters.fixparameters_.assert_any_call(parameters, rawdir=os.getcwd(), threads=24, output='mqpar-run.xml')
    subprocess.run.assert_any_call(
        ['sbatch', '--cpus-per-task=24', '--mem=120G', '--mail-type=END,FAIL',
         '--mail-user=christian.poitras@ircm.qc.ca',
         'maxquantcmd-mono.sh', str(output)], check=True)


def test_maxquant_mailenv(pytester, mock_testclass, mock_env_mail):
    parameters = Path(__file__).parent.joinpath('mqpar-windows.xml')
    output = 'mqpar-run.xml'
    FixParameters.fixparameters_ = MagicMock()
    subprocess.run = MagicMock()
    runner = CliRunner()
    result = runner.invoke(Maxquant.maxquant, ['--parameters', parameters])
    assert result.exit_code == 0
    FixParameters.fixparameters_.assert_any_call(parameters, rawdir=os.getcwd(), threads=24, output='mqpar-run.xml')
    subprocess.run.assert_any_call(
        ['sbatch', '--cpus-per-task=24', '--mem=120G', '--mail-type=END,FAIL',
         '--mail-user=christian.poitras@ircm.qc.ca',
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
    FixParameters.fixparameters_.assert_any_call(parameters, rawdir=os.getcwd(), threads=24, output='mqpar-run.xml')
    subprocess.run.assert_any_call(
        ['sbatch', '--cpus-per-task=24', '--mem=120G', '--mail-type=END,FAIL', '--mail-user=' + mail,
         'maxquantcmd-mono.sh',
         str(output)],
        check=True)
