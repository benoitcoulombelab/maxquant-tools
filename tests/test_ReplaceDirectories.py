import os
from pathlib import Path, PureWindowsPath
import shutil
import tempfile
import unittest

import click
from click.testing import CliRunner
from maxquanttools import ReplaceDirectories as rd
import xml.etree.ElementTree as ET


def test_replacedirectories_windows(testdir):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-windows.xml')
    dir = PureWindowsPath('C:\\home\\poitrac\\maxquant_test')
    fastadir = PureWindowsPath('C:\\home\\poitrac\\fastas')
    runner = CliRunner()
    result = runner.invoke(rd.replacedirectories, ['-p', parameters, '-d', str(dir), '-fd', str(fastadir)])
    assert 0 == result.exit_code
    root = ET.fromstring(result.output)
    assert fastadir.joinpath('SwissProt_Human_txid9606_20190424.fasta') == PureWindowsPath(root.find('.//fastaFilePath').text)
    assert dir.joinpath('OF_20190610_COU_01.raw') == PureWindowsPath(root.find('./filePaths/string[1]').text)
    assert dir.joinpath('OF_20190610_COU_02.raw') == PureWindowsPath(root.find('./filePaths/string[2]').text)
    assert '2' == root.find('.//numThreads').text
    assert 'False' == root.find('.//useDotNetCore').text
    assert 'True' == root.find('.//writeMzTab').text


def test_replacedirectories_windowsnofastadir(testdir):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-windows.xml')
    dir = PureWindowsPath('C:\\home\\poitrac\\maxquant_test')
    runner = CliRunner()
    result = runner.invoke(rd.replacedirectories, ['-p', parameters, '-d', str(dir)])
    assert 0 == result.exit_code
    root = ET.fromstring(result.output)
    assert dir.joinpath('SwissProt_Human_txid9606_20190424.fasta') == PureWindowsPath(root.find('.//fastaFilePath').text)
    assert dir.joinpath('OF_20190610_COU_01.raw') == PureWindowsPath(root.find('./filePaths/string[1]').text)
    assert dir.joinpath('OF_20190610_COU_02.raw') == PureWindowsPath(root.find('./filePaths/string[2]').text)
    assert '2' == root.find('.//numThreads').text
    assert 'False' == root.find('.//useDotNetCore').text
    assert 'True' == root.find('.//writeMzTab').text


def test_replacedirectories_windowsandthreads(testdir):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-windows.xml')
    dir = PureWindowsPath('C:\\home\\poitrac\\maxquant_test')
    fastadir = PureWindowsPath('C:\\home\\poitrac\\fastas')
    runner = CliRunner()
    result = runner.invoke(rd.replacedirectories, ['-p', parameters, '-d', str(dir), '-fd', str(fastadir), '-t', '4'])
    assert 0 == result.exit_code
    root = ET.fromstring(result.output)
    assert fastadir.joinpath('SwissProt_Human_txid9606_20190424.fasta') == PureWindowsPath(root.find('.//fastaFilePath').text)
    assert dir.joinpath('OF_20190610_COU_01.raw') == PureWindowsPath(root.find('./filePaths/string[1]').text)
    assert dir.joinpath('OF_20190610_COU_02.raw') == PureWindowsPath(root.find('./filePaths/string[2]').text)
    assert '4' == root.find('.//numThreads').text
    assert 'False' == root.find('.//useDotNetCore').text
    assert 'True' == root.find('.//writeMzTab').text


def test_replacedirectories_windows2linux(testdir):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-windows.xml')
    dir = Path('/home/poitrac/maxquant_test')
    fastadir = Path('/home/poitrac/fastas')
    runner = CliRunner()
    result = runner.invoke(rd.replacedirectories, ['-p', parameters, '-d', str(dir), '-fd', str(fastadir)])
    assert 0 == result.exit_code
    root = ET.fromstring(result.output)
    assert fastadir.joinpath('SwissProt_Human_txid9606_20190424.fasta'), Path(root.find('.//fastaFilePath').text)
    assert dir.joinpath('OF_20190610_COU_01.raw') == Path(root.find('./filePaths/string[1]').text)
    assert dir.joinpath('OF_20190610_COU_02.raw') == Path(root.find('./filePaths/string[2]').text)
    assert '2' == root.find('.//numThreads').text
    assert 'False' == root.find('.//useDotNetCore').text
    assert 'True' == root.find('.//writeMzTab').text


def test_replacedirectories_windowskeepcore(testdir):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-windows.xml')
    dir = PureWindowsPath('C:\\home\\poitrac\\maxquant_test')
    fastadir = PureWindowsPath('C:\\home\\poitrac\\fastas')
    runner = CliRunner()
    result = runner.invoke(rd.replacedirectories, ['-p', parameters, '-d', str(dir), '-fd', str(fastadir), '--keep-core'])
    assert 0 == result.exit_code
    root = ET.fromstring(result.output)
    assert fastadir.joinpath('SwissProt_Human_txid9606_20190424.fasta') == PureWindowsPath(root.find('.//fastaFilePath').text)
    assert dir.joinpath('OF_20190610_COU_01.raw') == PureWindowsPath(root.find('./filePaths/string[1]').text)
    assert dir.joinpath('OF_20190610_COU_02.raw') == PureWindowsPath(root.find('./filePaths/string[2]').text)
    assert '2' == root.find('.//numThreads').text
    assert 'True' == root.find('.//useDotNetCore').text
    assert 'True' == root.find('.//writeMzTab').text


def test_replacedirectories_windows2linuxnofastadir(testdir):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-windows.xml')
    dir = Path('/home/poitrac/maxquant_test')
    runner = CliRunner()
    result = runner.invoke(rd.replacedirectories, ['-p', parameters, '-d', str(dir)])
    assert 0 == result.exit_code
    root = ET.fromstring(result.output)
    assert dir.joinpath('SwissProt_Human_txid9606_20190424.fasta') == Path(root.find('.//fastaFilePath').text)
    assert dir.joinpath('OF_20190610_COU_01.raw') == Path(root.find('./filePaths/string[1]').text)
    assert dir.joinpath('OF_20190610_COU_02.raw') == Path(root.find('./filePaths/string[2]').text)
    assert '2' == root.find('.//numThreads').text
    assert 'False' == root.find('.//useDotNetCore').text
    assert 'True' == root.find('.//writeMzTab').text


def test_replacedirectories_windows2linuxandthreads(testdir):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-windows.xml')
    dir = Path('/home/poitrac/maxquant_test')
    fastadir = Path('/home/poitrac/fastas')
    runner = CliRunner()
    result = runner.invoke(rd.replacedirectories, ['-p', parameters, '-d', str(dir), '-fd', str(fastadir), '-t', '4'])
    assert 0 == result.exit_code
    root = ET.fromstring(result.output)
    assert fastadir.joinpath('SwissProt_Human_txid9606_20190424.fasta'), Path(root.find('.//fastaFilePath').text)
    assert dir.joinpath('OF_20190610_COU_01.raw') == Path(root.find('./filePaths/string[1]').text)
    assert dir.joinpath('OF_20190610_COU_02.raw') == Path(root.find('./filePaths/string[2]').text)
    assert '4' == root.find('.//numThreads').text
    assert 'False' == root.find('.//useDotNetCore').text
    assert 'True' == root.find('.//writeMzTab').text


def test_replacedirectories_linux(testdir):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-linux.xml')
    dir = Path('/home/poitrac/maxquant_test')
    fastadir = Path('/home/poitrac/fastas')
    runner = CliRunner()
    result = runner.invoke(rd.replacedirectories, ['-p', parameters, '-d', str(dir), '-fd', str(fastadir)])
    assert 0 == result.exit_code
    root = ET.fromstring(result.output)
    assert fastadir.joinpath('SwissProt_Human_txid9606_20190424.fasta') == Path(root.find('.//fastaFilePath').text)
    assert dir.joinpath('OF_20190610_COU_01.raw') == Path(root.find('./filePaths/string[1]').text)
    assert dir.joinpath('OF_20190610_COU_02.raw') == Path(root.find('./filePaths/string[2]').text)
    assert '2' == root.find('.//numThreads').text
    assert 'False' == root.find('.//useDotNetCore').text
    assert 'True' == root.find('.//writeMzTab').text


def test_replacedirectories_linuxnofastadir(testdir):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-linux.xml')
    dir = Path('/home/poitrac/maxquant_test')
    runner = CliRunner()
    result = runner.invoke(rd.replacedirectories, ['-p', parameters, '-d', str(dir)])
    assert 0 == result.exit_code
    root = ET.fromstring(result.output)
    assert dir.joinpath('SwissProt_Human_txid9606_20190424.fasta') == Path(root.find('.//fastaFilePath').text)
    assert dir.joinpath('OF_20190610_COU_01.raw') == Path(root.find('./filePaths/string[1]').text)
    assert dir.joinpath('OF_20190610_COU_02.raw') == Path(root.find('./filePaths/string[2]').text)
    assert '2' == root.find('.//numThreads').text
    assert 'False' == root.find('.//useDotNetCore').text
    assert 'True' == root.find('.//writeMzTab').text


def test_replacedirectories_linuxandthreads(testdir):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-linux.xml')
    dir = Path('/home/poitrac/maxquant_test')
    fastadir = Path('/home/poitrac/fastas')
    runner = CliRunner()
    result = runner.invoke(rd.replacedirectories, ['-p', parameters, '-d', str(dir), '-fd', str(fastadir), '-t', '4'])
    assert 0 == result.exit_code
    root = ET.fromstring(result.output)
    assert fastadir.joinpath('SwissProt_Human_txid9606_20190424.fasta') == Path(root.find('.//fastaFilePath').text)
    assert dir.joinpath('OF_20190610_COU_01.raw') == Path(root.find('./filePaths/string[1]').text)
    assert dir.joinpath('OF_20190610_COU_02.raw') == Path(root.find('./filePaths/string[2]').text)
    assert '4' == root.find('.//numThreads').text
    assert 'False' == root.find('.//useDotNetCore').text
    assert 'True' == root.find('.//writeMzTab').text


def test_replacedirectories_linux2windowds(testdir):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-linux.xml')
    dir = PureWindowsPath('C:\\home\\poitrac\\maxquant_test')
    fastadir = PureWindowsPath('C:\\home\\poitrac\\fastas')
    runner = CliRunner()
    result = runner.invoke(rd.replacedirectories, ['-p', parameters, '-d', str(dir), '-fd', str(fastadir)])
    assert 0 == result.exit_code
    root = ET.fromstring(result.output)
    assert fastadir.joinpath('SwissProt_Human_txid9606_20190424.fasta') == PureWindowsPath(root.find('.//fastaFilePath').text)
    assert dir.joinpath('OF_20190610_COU_01.raw') == PureWindowsPath(root.find('./filePaths/string[1]').text)
    assert dir.joinpath('OF_20190610_COU_02.raw') == PureWindowsPath(root.find('./filePaths/string[2]').text)
    assert '2' == root.find('.//numThreads').text
    assert 'False' == root.find('.//useDotNetCore').text
    assert 'True' == root.find('.//writeMzTab').text


def test_replacedirectories_linux2windowdsnofastadir(testdir):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-linux.xml')
    dir = PureWindowsPath('C:\\home\\poitrac\\maxquant_test')
    runner = CliRunner()
    result = runner.invoke(rd.replacedirectories, ['-p', parameters, '-d', str(dir)])
    assert 0 == result.exit_code
    root = ET.fromstring(result.output)
    assert dir.joinpath('SwissProt_Human_txid9606_20190424.fasta') == PureWindowsPath(root.find('.//fastaFilePath').text)
    assert dir.joinpath('OF_20190610_COU_01.raw') == PureWindowsPath(root.find('./filePaths/string[1]').text)
    assert dir.joinpath('OF_20190610_COU_02.raw') == PureWindowsPath(root.find('./filePaths/string[2]').text)
    assert '2' == root.find('.//numThreads').text
    assert 'False' == root.find('.//useDotNetCore').text
    assert 'True' == root.find('.//writeMzTab').text


def test_replacedirectories_linux2windowdsandthreads(testdir):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-linux.xml')
    dir = PureWindowsPath('C:\\home\\poitrac\\maxquant_test')
    fastadir = PureWindowsPath('C:\\home\\poitrac\\fastas')
    runner = CliRunner()
    result = runner.invoke(rd.replacedirectories, ['-p', parameters, '-d', str(dir), '-fd', str(fastadir), '-t', '4'])
    assert 0 == result.exit_code
    root = ET.fromstring(result.output)
    assert fastadir.joinpath('SwissProt_Human_txid9606_20190424.fasta') == PureWindowsPath(root.find('.//fastaFilePath').text)
    assert dir.joinpath('OF_20190610_COU_01.raw') == PureWindowsPath(root.find('./filePaths/string[1]').text)
    assert dir.joinpath('OF_20190610_COU_02.raw') == PureWindowsPath(root.find('./filePaths/string[2]').text)
    assert '4' == root.find('.//numThreads').text
    assert 'False' == root.find('.//useDotNetCore').text
    assert 'True' == root.find('.//writeMzTab').text
