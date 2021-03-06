from pathlib import Path, PureWindowsPath
from xml.etree import ElementTree

from click.testing import CliRunner

from maxquanttools import FixParameters


def test_fixparameters_windows(testdir):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-windows.xml')
    rawdir = PureWindowsPath('C:\\home\\poitrac\\maxquant_test')
    fastadir = PureWindowsPath('C:\\home\\poitrac\\fastas')
    runner = CliRunner()
    result = runner.invoke(FixParameters.fixparameters, ['-p', parameters, '-d', str(rawdir), '-fd', str(fastadir)])
    assert 0 == result.exit_code
    root = ElementTree.fromstring(result.output)
    assert fastadir.joinpath('SwissProt_Human_txid9606_20190424.fasta') == PureWindowsPath(
        root.find('.//fastaFilePath').text)
    assert rawdir.joinpath('OF_20190610_COU_01.raw') == PureWindowsPath(root.find('./filePaths/string[1]').text)
    assert rawdir.joinpath('OF_20190610_COU_02.raw') == PureWindowsPath(root.find('./filePaths/string[2]').text)
    assert '2' == root.find('.//numThreads').text
    assert 'False' == root.find('.//useDotNetCore').text
    assert 'True' == root.find('.//writeMzTab').text


def test_fixparameters_windowsnofastadir(testdir):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-windows.xml')
    rawdir = PureWindowsPath('C:\\home\\poitrac\\maxquant_test')
    runner = CliRunner()
    result = runner.invoke(FixParameters.fixparameters, ['-p', parameters, '-d', str(rawdir)])
    assert 0 == result.exit_code
    root = ElementTree.fromstring(result.output)
    assert rawdir.joinpath('SwissProt_Human_txid9606_20190424.fasta') == PureWindowsPath(
        root.find('.//fastaFilePath').text)
    assert rawdir.joinpath('OF_20190610_COU_01.raw') == PureWindowsPath(root.find('./filePaths/string[1]').text)
    assert rawdir.joinpath('OF_20190610_COU_02.raw') == PureWindowsPath(root.find('./filePaths/string[2]').text)
    assert '2' == root.find('.//numThreads').text
    assert 'False' == root.find('.//useDotNetCore').text
    assert 'True' == root.find('.//writeMzTab').text


def test_fixparameters_windowsandthreads(testdir):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-windows.xml')
    rawdir = PureWindowsPath('C:\\home\\poitrac\\maxquant_test')
    fastadir = PureWindowsPath('C:\\home\\poitrac\\fastas')
    runner = CliRunner()
    result = runner.invoke(FixParameters.fixparameters,
                           ['-p', parameters, '-d', str(rawdir), '-fd', str(fastadir), '-t', '4'])
    assert 0 == result.exit_code
    root = ElementTree.fromstring(result.output)
    assert fastadir.joinpath('SwissProt_Human_txid9606_20190424.fasta') == PureWindowsPath(
        root.find('.//fastaFilePath').text)
    assert rawdir.joinpath('OF_20190610_COU_01.raw') == PureWindowsPath(root.find('./filePaths/string[1]').text)
    assert rawdir.joinpath('OF_20190610_COU_02.raw') == PureWindowsPath(root.find('./filePaths/string[2]').text)
    assert '4' == root.find('.//numThreads').text
    assert 'False' == root.find('.//useDotNetCore').text
    assert 'True' == root.find('.//writeMzTab').text


def test_fixparameters_windows2linux(testdir):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-windows.xml')
    rawdir = Path('/home/poitrac/maxquant_test')
    fastadir = Path('/home/poitrac/fastas')
    runner = CliRunner()
    result = runner.invoke(FixParameters.fixparameters, ['-p', parameters, '-d', str(rawdir), '-fd', str(fastadir)])
    assert 0 == result.exit_code
    root = ElementTree.fromstring(result.output)
    assert fastadir.joinpath('SwissProt_Human_txid9606_20190424.fasta'), Path(root.find('.//fastaFilePath').text)
    assert rawdir.joinpath('OF_20190610_COU_01.raw') == Path(root.find('./filePaths/string[1]').text)
    assert rawdir.joinpath('OF_20190610_COU_02.raw') == Path(root.find('./filePaths/string[2]').text)
    assert '2' == root.find('.//numThreads').text
    assert 'False' == root.find('.//useDotNetCore').text
    assert 'True' == root.find('.//writeMzTab').text


def test_fixparameters_windowskeepcore(testdir):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-windows.xml')
    rawdir = PureWindowsPath('C:\\home\\poitrac\\maxquant_test')
    fastadir = PureWindowsPath('C:\\home\\poitrac\\fastas')
    runner = CliRunner()
    result = runner.invoke(FixParameters.fixparameters,
                           ['-p', parameters, '-d', str(rawdir), '-fd', str(fastadir), '--keep-core'])
    assert 0 == result.exit_code
    root = ElementTree.fromstring(result.output)
    assert fastadir.joinpath('SwissProt_Human_txid9606_20190424.fasta') == PureWindowsPath(
        root.find('.//fastaFilePath').text)
    assert rawdir.joinpath('OF_20190610_COU_01.raw') == PureWindowsPath(root.find('./filePaths/string[1]').text)
    assert rawdir.joinpath('OF_20190610_COU_02.raw') == PureWindowsPath(root.find('./filePaths/string[2]').text)
    assert '2' == root.find('.//numThreads').text
    assert 'True' == root.find('.//useDotNetCore').text
    assert 'True' == root.find('.//writeMzTab').text


def test_fixparameters_windows2linuxnofastadir(testdir):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-windows.xml')
    rawdir = Path('/home/poitrac/maxquant_test')
    runner = CliRunner()
    result = runner.invoke(FixParameters.fixparameters, ['-p', parameters, '-d', str(rawdir)])
    assert 0 == result.exit_code
    root = ElementTree.fromstring(result.output)
    assert rawdir.joinpath('SwissProt_Human_txid9606_20190424.fasta') == Path(root.find('.//fastaFilePath').text)
    assert rawdir.joinpath('OF_20190610_COU_01.raw') == Path(root.find('./filePaths/string[1]').text)
    assert rawdir.joinpath('OF_20190610_COU_02.raw') == Path(root.find('./filePaths/string[2]').text)
    assert '2' == root.find('.//numThreads').text
    assert 'False' == root.find('.//useDotNetCore').text
    assert 'True' == root.find('.//writeMzTab').text


def test_fixparameters_windows2linuxandthreads(testdir):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-windows.xml')
    rawdir = Path('/home/poitrac/maxquant_test')
    fastadir = Path('/home/poitrac/fastas')
    runner = CliRunner()
    result = runner.invoke(FixParameters.fixparameters,
                           ['-p', parameters, '-d', str(rawdir), '-fd', str(fastadir), '-t', '4'])
    assert 0 == result.exit_code
    root = ElementTree.fromstring(result.output)
    assert fastadir.joinpath('SwissProt_Human_txid9606_20190424.fasta'), Path(root.find('.//fastaFilePath').text)
    assert rawdir.joinpath('OF_20190610_COU_01.raw') == Path(root.find('./filePaths/string[1]').text)
    assert rawdir.joinpath('OF_20190610_COU_02.raw') == Path(root.find('./filePaths/string[2]').text)
    assert '4' == root.find('.//numThreads').text
    assert 'False' == root.find('.//useDotNetCore').text
    assert 'True' == root.find('.//writeMzTab').text


def test_fixparameters_linux(testdir):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-linux.xml')
    rawdir = Path('/home/poitrac/maxquant_test')
    fastadir = Path('/home/poitrac/fastas')
    runner = CliRunner()
    result = runner.invoke(FixParameters.fixparameters, ['-p', parameters, '-d', str(rawdir), '-fd', str(fastadir)])
    assert 0 == result.exit_code
    root = ElementTree.fromstring(result.output)
    assert fastadir.joinpath('SwissProt_Human_txid9606_20190424.fasta') == Path(root.find('.//fastaFilePath').text)
    assert rawdir.joinpath('OF_20190610_COU_01.raw') == Path(root.find('./filePaths/string[1]').text)
    assert rawdir.joinpath('OF_20190610_COU_02.raw') == Path(root.find('./filePaths/string[2]').text)
    assert '2' == root.find('.//numThreads').text
    assert 'False' == root.find('.//useDotNetCore').text
    assert 'True' == root.find('.//writeMzTab').text


def test_fixparameters_linuxnofastadir(testdir):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-linux.xml')
    rawdir = Path('/home/poitrac/maxquant_test')
    runner = CliRunner()
    result = runner.invoke(FixParameters.fixparameters, ['-p', parameters, '-d', str(rawdir)])
    assert 0 == result.exit_code
    root = ElementTree.fromstring(result.output)
    assert rawdir.joinpath('SwissProt_Human_txid9606_20190424.fasta') == Path(root.find('.//fastaFilePath').text)
    assert rawdir.joinpath('OF_20190610_COU_01.raw') == Path(root.find('./filePaths/string[1]').text)
    assert rawdir.joinpath('OF_20190610_COU_02.raw') == Path(root.find('./filePaths/string[2]').text)
    assert '2' == root.find('.//numThreads').text
    assert 'False' == root.find('.//useDotNetCore').text
    assert 'True' == root.find('.//writeMzTab').text


def test_fixparameters_linuxandthreads(testdir):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-linux.xml')
    rawdir = Path('/home/poitrac/maxquant_test')
    fastadir = Path('/home/poitrac/fastas')
    runner = CliRunner()
    result = runner.invoke(FixParameters.fixparameters,
                           ['-p', parameters, '-d', str(rawdir), '-fd', str(fastadir), '-t', '4'])
    assert 0 == result.exit_code
    root = ElementTree.fromstring(result.output)
    assert fastadir.joinpath('SwissProt_Human_txid9606_20190424.fasta') == Path(root.find('.//fastaFilePath').text)
    assert rawdir.joinpath('OF_20190610_COU_01.raw') == Path(root.find('./filePaths/string[1]').text)
    assert rawdir.joinpath('OF_20190610_COU_02.raw') == Path(root.find('./filePaths/string[2]').text)
    assert '4' == root.find('.//numThreads').text
    assert 'False' == root.find('.//useDotNetCore').text
    assert 'True' == root.find('.//writeMzTab').text


def test_fixparameters_linux2windowds(testdir):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-linux.xml')
    rawdir = PureWindowsPath('C:\\home\\poitrac\\maxquant_test')
    fastadir = PureWindowsPath('C:\\home\\poitrac\\fastas')
    runner = CliRunner()
    result = runner.invoke(FixParameters.fixparameters, ['-p', parameters, '-d', str(rawdir), '-fd', str(fastadir)])
    assert 0 == result.exit_code
    root = ElementTree.fromstring(result.output)
    assert fastadir.joinpath('SwissProt_Human_txid9606_20190424.fasta') == PureWindowsPath(
        root.find('.//fastaFilePath').text)
    assert rawdir.joinpath('OF_20190610_COU_01.raw') == PureWindowsPath(root.find('./filePaths/string[1]').text)
    assert rawdir.joinpath('OF_20190610_COU_02.raw') == PureWindowsPath(root.find('./filePaths/string[2]').text)
    assert '2' == root.find('.//numThreads').text
    assert 'False' == root.find('.//useDotNetCore').text
    assert 'True' == root.find('.//writeMzTab').text


def test_fixparameters_linux2windowdsnofastadir(testdir):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-linux.xml')
    rawdir = PureWindowsPath('C:\\home\\poitrac\\maxquant_test')
    runner = CliRunner()
    result = runner.invoke(FixParameters.fixparameters, ['-p', parameters, '-d', str(rawdir)])
    assert 0 == result.exit_code
    root = ElementTree.fromstring(result.output)
    assert rawdir.joinpath('SwissProt_Human_txid9606_20190424.fasta') == PureWindowsPath(
        root.find('.//fastaFilePath').text)
    assert rawdir.joinpath('OF_20190610_COU_01.raw') == PureWindowsPath(root.find('./filePaths/string[1]').text)
    assert rawdir.joinpath('OF_20190610_COU_02.raw') == PureWindowsPath(root.find('./filePaths/string[2]').text)
    assert '2' == root.find('.//numThreads').text
    assert 'False' == root.find('.//useDotNetCore').text
    assert 'True' == root.find('.//writeMzTab').text


def test_fixparameters_linux2windowdsandthreads(testdir):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-linux.xml')
    rawdir = PureWindowsPath('C:\\home\\poitrac\\maxquant_test')
    fastadir = PureWindowsPath('C:\\home\\poitrac\\fastas')
    runner = CliRunner()
    result = runner.invoke(FixParameters.fixparameters,
                           ['-p', parameters, '-d', str(rawdir), '-fd', str(fastadir), '-t', '4'])
    assert 0 == result.exit_code
    root = ElementTree.fromstring(result.output)
    assert fastadir.joinpath('SwissProt_Human_txid9606_20190424.fasta') == PureWindowsPath(
        root.find('.//fastaFilePath').text)
    assert rawdir.joinpath('OF_20190610_COU_01.raw') == PureWindowsPath(root.find('./filePaths/string[1]').text)
    assert rawdir.joinpath('OF_20190610_COU_02.raw') == PureWindowsPath(root.find('./filePaths/string[2]').text)
    assert '4' == root.find('.//numThreads').text
    assert 'False' == root.find('.//useDotNetCore').text
    assert 'True' == root.find('.//writeMzTab').text
