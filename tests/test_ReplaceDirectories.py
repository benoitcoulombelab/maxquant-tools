import os
from pathlib import Path, PureWindowsPath
import shutil
import tempfile
import unittest

import click
from click.testing import CliRunner
from maxquantparameters import ReplaceDirectories
import xml.etree.ElementTree as ET


class TestReplaceDirectories(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_main_windows(self):
        parent = Path(__file__).parent
        parameters = parent.joinpath('mqpar-windows.xml')
        dir = PureWindowsPath('C:\\home\\poitrac\\maxquant_test')
        fastadir = PureWindowsPath('C:\\home\\poitrac\\fastas')
        runner = CliRunner()
        result = runner.invoke(ReplaceDirectories.main, ['-p', parameters, '-d', str(dir), '-fd', str(fastadir)])
        self.assertEqual(0, result.exit_code)
        root = ET.fromstring(result.output)
        self.assertEqual(fastadir.joinpath('SwissProt_Human_txid9606_20190424.fasta'), PureWindowsPath(root.find('.//fastaFilePath').text))
        self.assertEqual(dir.joinpath('OF_20190610_COU_01.raw'), PureWindowsPath(root.find('./filePaths/string[1]').text))
        self.assertEqual(dir.joinpath('OF_20190610_COU_02.raw'), PureWindowsPath(root.find('./filePaths/string[2]').text))
        self.assertEqual('2', root.find('.//numThreads').text)

    def test_main_windowsnofastadir(self):
        parent = Path(__file__).parent
        parameters = parent.joinpath('mqpar-windows.xml')
        dir = PureWindowsPath('C:\\home\\poitrac\\maxquant_test')
        runner = CliRunner()
        result = runner.invoke(ReplaceDirectories.main, ['-p', parameters, '-d', str(dir)])
        self.assertEqual(0, result.exit_code)
        root = ET.fromstring(result.output)
        self.assertEqual(dir.joinpath('SwissProt_Human_txid9606_20190424.fasta'), PureWindowsPath(root.find('.//fastaFilePath').text))
        self.assertEqual(dir.joinpath('OF_20190610_COU_01.raw'), PureWindowsPath(root.find('./filePaths/string[1]').text))
        self.assertEqual(dir.joinpath('OF_20190610_COU_02.raw'), PureWindowsPath(root.find('./filePaths/string[2]').text))
        self.assertEqual('2', root.find('.//numThreads').text)

    def test_main_windowsandthreads(self):
        parent = Path(__file__).parent
        parameters = parent.joinpath('mqpar-windows.xml')
        dir = PureWindowsPath('C:\\home\\poitrac\\maxquant_test')
        fastadir = PureWindowsPath('C:\\home\\poitrac\\fastas')
        runner = CliRunner()
        result = runner.invoke(ReplaceDirectories.main, ['-p', parameters, '-d', str(dir), '-fd', str(fastadir), '-t', '4'])
        self.assertEqual(0, result.exit_code)
        root = ET.fromstring(result.output)
        self.assertEqual(fastadir.joinpath('SwissProt_Human_txid9606_20190424.fasta'), PureWindowsPath(root.find('.//fastaFilePath').text))
        self.assertEqual(dir.joinpath('OF_20190610_COU_01.raw'), PureWindowsPath(root.find('./filePaths/string[1]').text))
        self.assertEqual(dir.joinpath('OF_20190610_COU_02.raw'), PureWindowsPath(root.find('./filePaths/string[2]').text))
        self.assertEqual('4', root.find('.//numThreads').text)

    def test_main_windows2linux(self):
        parent = Path(__file__).parent
        parameters = parent.joinpath('mqpar-windows.xml')
        dir = Path('/home/poitrac/maxquant_test')
        fastadir = Path('/home/poitrac/fastas')
        runner = CliRunner()
        result = runner.invoke(ReplaceDirectories.main, ['-p', parameters, '-d', str(dir), '-fd', str(fastadir)])
        self.assertEqual(0, result.exit_code)
        root = ET.fromstring(result.output)
        self.assertEqual(fastadir.joinpath('SwissProt_Human_txid9606_20190424.fasta'), Path(root.find('.//fastaFilePath').text))
        self.assertEqual(dir.joinpath('OF_20190610_COU_01.raw'), Path(root.find('./filePaths/string[1]').text))
        self.assertEqual(dir.joinpath('OF_20190610_COU_02.raw'), Path(root.find('./filePaths/string[2]').text))
        self.assertEqual('2', root.find('.//numThreads').text)

    def test_main_windows2linuxnofastadir(self):
        parent = Path(__file__).parent
        parameters = parent.joinpath('mqpar-windows.xml')
        dir = Path('/home/poitrac/maxquant_test')
        runner = CliRunner()
        result = runner.invoke(ReplaceDirectories.main, ['-p', parameters, '-d', str(dir)])
        self.assertEqual(0, result.exit_code)
        root = ET.fromstring(result.output)
        self.assertEqual(dir.joinpath('SwissProt_Human_txid9606_20190424.fasta'), Path(root.find('.//fastaFilePath').text))
        self.assertEqual(dir.joinpath('OF_20190610_COU_01.raw'), Path(root.find('./filePaths/string[1]').text))
        self.assertEqual(dir.joinpath('OF_20190610_COU_02.raw'), Path(root.find('./filePaths/string[2]').text))
        self.assertEqual('2', root.find('.//numThreads').text)

    def test_main_windows2linuxandthreads(self):
        parent = Path(__file__).parent
        parameters = parent.joinpath('mqpar-windows.xml')
        dir = Path('/home/poitrac/maxquant_test')
        fastadir = Path('/home/poitrac/fastas')
        runner = CliRunner()
        result = runner.invoke(ReplaceDirectories.main, ['-p', parameters, '-d', str(dir), '-fd', str(fastadir), '-t', '4'])
        self.assertEqual(0, result.exit_code)
        root = ET.fromstring(result.output)
        self.assertEqual(fastadir.joinpath('SwissProt_Human_txid9606_20190424.fasta'), Path(root.find('.//fastaFilePath').text))
        self.assertEqual(dir.joinpath('OF_20190610_COU_01.raw'), Path(root.find('./filePaths/string[1]').text))
        self.assertEqual(dir.joinpath('OF_20190610_COU_02.raw'), Path(root.find('./filePaths/string[2]').text))
        self.assertEqual('4', root.find('.//numThreads').text)

    def test_main_linux(self):
        parent = Path(__file__).parent
        parameters = parent.joinpath('mqpar-linux.xml')
        dir = Path('/home/poitrac/maxquant_test')
        fastadir = Path('/home/poitrac/fastas')
        runner = CliRunner()
        result = runner.invoke(ReplaceDirectories.main, ['-p', parameters, '-d', str(dir), '-fd', str(fastadir)])
        self.assertEqual(0, result.exit_code)
        root = ET.fromstring(result.output)
        self.assertEqual(fastadir.joinpath('SwissProt_Human_txid9606_20190424.fasta'), Path(root.find('.//fastaFilePath').text))
        self.assertEqual(dir.joinpath('OF_20190610_COU_01.raw'), Path(root.find('./filePaths/string[1]').text))
        self.assertEqual(dir.joinpath('OF_20190610_COU_02.raw'), Path(root.find('./filePaths/string[2]').text))
        self.assertEqual('2', root.find('.//numThreads').text)

    def test_main_linuxnofastadir(self):
        parent = Path(__file__).parent
        parameters = parent.joinpath('mqpar-linux.xml')
        dir = Path('/home/poitrac/maxquant_test')
        runner = CliRunner()
        result = runner.invoke(ReplaceDirectories.main, ['-p', parameters, '-d', str(dir)])
        self.assertEqual(0, result.exit_code)
        root = ET.fromstring(result.output)
        self.assertEqual(dir.joinpath('SwissProt_Human_txid9606_20190424.fasta'), Path(root.find('.//fastaFilePath').text))
        self.assertEqual(dir.joinpath('OF_20190610_COU_01.raw'), Path(root.find('./filePaths/string[1]').text))
        self.assertEqual(dir.joinpath('OF_20190610_COU_02.raw'), Path(root.find('./filePaths/string[2]').text))
        self.assertEqual('2', root.find('.//numThreads').text)

    def test_main_linuxandthreads(self):
        parent = Path(__file__).parent
        parameters = parent.joinpath('mqpar-linux.xml')
        dir = Path('/home/poitrac/maxquant_test')
        fastadir = Path('/home/poitrac/fastas')
        runner = CliRunner()
        result = runner.invoke(ReplaceDirectories.main, ['-p', parameters, '-d', str(dir), '-fd', str(fastadir), '-t', '4'])
        self.assertEqual(0, result.exit_code)
        root = ET.fromstring(result.output)
        self.assertEqual(fastadir.joinpath('SwissProt_Human_txid9606_20190424.fasta'), Path(root.find('.//fastaFilePath').text))
        self.assertEqual(dir.joinpath('OF_20190610_COU_01.raw'), Path(root.find('./filePaths/string[1]').text))
        self.assertEqual(dir.joinpath('OF_20190610_COU_02.raw'), Path(root.find('./filePaths/string[2]').text))
        self.assertEqual('4', root.find('.//numThreads').text)

    def test_main_linux2windowds(self):
        parent = Path(__file__).parent
        parameters = parent.joinpath('mqpar-linux.xml')
        dir = PureWindowsPath('C:\\home\\poitrac\\maxquant_test')
        fastadir = PureWindowsPath('C:\\home\\poitrac\\fastas')
        runner = CliRunner()
        result = runner.invoke(ReplaceDirectories.main, ['-p', parameters, '-d', str(dir), '-fd', str(fastadir)])
        self.assertEqual(0, result.exit_code)
        root = ET.fromstring(result.output)
        self.assertEqual(fastadir.joinpath('SwissProt_Human_txid9606_20190424.fasta'), PureWindowsPath(root.find('.//fastaFilePath').text))
        self.assertEqual(dir.joinpath('OF_20190610_COU_01.raw'), PureWindowsPath(root.find('./filePaths/string[1]').text))
        self.assertEqual(dir.joinpath('OF_20190610_COU_02.raw'), PureWindowsPath(root.find('./filePaths/string[2]').text))
        self.assertEqual('2', root.find('.//numThreads').text)

    def test_main_linux2windowdsnofastadir(self):
        parent = Path(__file__).parent
        parameters = parent.joinpath('mqpar-linux.xml')
        dir = PureWindowsPath('C:\\home\\poitrac\\maxquant_test')
        runner = CliRunner()
        result = runner.invoke(ReplaceDirectories.main, ['-p', parameters, '-d', str(dir)])
        self.assertEqual(0, result.exit_code)
        root = ET.fromstring(result.output)
        self.assertEqual(dir.joinpath('SwissProt_Human_txid9606_20190424.fasta'), PureWindowsPath(root.find('.//fastaFilePath').text))
        self.assertEqual(dir.joinpath('OF_20190610_COU_01.raw'), PureWindowsPath(root.find('./filePaths/string[1]').text))
        self.assertEqual(dir.joinpath('OF_20190610_COU_02.raw'), PureWindowsPath(root.find('./filePaths/string[2]').text))
        self.assertEqual('2', root.find('.//numThreads').text)

    def test_main_linux2windowdsandthreads(self):
        parent = Path(__file__).parent
        parameters = parent.joinpath('mqpar-linux.xml')
        dir = PureWindowsPath('C:\\home\\poitrac\\maxquant_test')
        fastadir = PureWindowsPath('C:\\home\\poitrac\\fastas')
        runner = CliRunner()
        result = runner.invoke(ReplaceDirectories.main, ['-p', parameters, '-d', str(dir), '-fd', str(fastadir), '-t', '4'])
        self.assertEqual(0, result.exit_code)
        root = ET.fromstring(result.output)
        self.assertEqual(fastadir.joinpath('SwissProt_Human_txid9606_20190424.fasta'), PureWindowsPath(root.find('.//fastaFilePath').text))
        self.assertEqual(dir.joinpath('OF_20190610_COU_01.raw'), PureWindowsPath(root.find('./filePaths/string[1]').text))
        self.assertEqual(dir.joinpath('OF_20190610_COU_02.raw'), PureWindowsPath(root.find('./filePaths/string[2]').text))
        self.assertEqual('4', root.find('.//numThreads').text)


if __name__ == '__main__':
    unittest.main()
