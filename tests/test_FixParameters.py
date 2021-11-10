from pathlib import Path, PureWindowsPath
from xml.etree import ElementTree

from click.testing import CliRunner

from maxquanttools import FixParameters


def test_fixparameters_relativepaths(pytester):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-windows.xml')
    rawdir = Path('maxquant_test')
    fastadir = Path('fastas')
    diadir = Path('dia')
    runner = CliRunner()
    result = runner.invoke(FixParameters.fixparameters,
                           ['-p', parameters, '-d', str(rawdir), '-fd', str(fastadir), '--diadir', str(diadir)])
    assert result.exit_code == 0
    root = ElementTree.fromstring(result.output)
    assert Path(root.find('.//fastaFilePath').text) == pytester.path.joinpath(fastadir).joinpath(
        'SwissProt_Human_txid9606_20190424.fasta')
    assert Path(root.find('./filePaths/string[1]').text) == pytester.path.joinpath(rawdir).joinpath(
        'OF_20190610_COU_01.raw')
    assert Path(root.find('./filePaths/string[2]').text) == pytester.path.joinpath(rawdir).joinpath(
        'OF_20190610_COU_02.raw')
    assert Path(root.find('.//diaLibraryPath/string[1]').text) == pytester.path.joinpath(diadir).joinpath(
        'spectral_library.tsv')
    assert Path(root.find('.//diaPeptidePaths/string[1]').text) == pytester.path.joinpath(diadir).joinpath(
        'peptides.txt')
    assert Path(root.find('.//diaEvidencePaths/string[1]').text) == pytester.path.joinpath(diadir).joinpath(
        'evidence.txt')
    assert Path(root.find('.//diaMsmsPaths/string[1]').text) == pytester.path.joinpath(diadir).joinpath('msms.txt')
    assert root.find('.//numThreads').text == '2'
    assert root.find('.//useDotNetCore').text == 'False'
    assert root.find('.//writeMzTab').text == 'True'


def test_fixparameters_windows(pytester):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-windows.xml')
    rawdir = PureWindowsPath('C:\\home\\poitrac\\maxquant_test')
    fastadir = PureWindowsPath('C:\\home\\poitrac\\fastas')
    diadir = PureWindowsPath('C:\\home\\poitrac\\dia')
    runner = CliRunner()
    result = runner.invoke(FixParameters.fixparameters,
                           ['-p', parameters, '-d', str(rawdir), '-fd', str(fastadir), '--diadir', str(diadir)])
    assert result.exit_code == 0
    root = ElementTree.fromstring(result.output)
    assert PureWindowsPath(root.find('.//fastaFilePath').text) == fastadir.joinpath(
        'SwissProt_Human_txid9606_20190424.fasta')
    assert PureWindowsPath(root.find('./filePaths/string[1]').text) == rawdir.joinpath('OF_20190610_COU_01.raw')
    assert PureWindowsPath(root.find('./filePaths/string[2]').text) == rawdir.joinpath('OF_20190610_COU_02.raw')
    assert PureWindowsPath(root.find('.//diaLibraryPath/string[1]').text) == diadir.joinpath('spectral_library.tsv')
    assert PureWindowsPath(root.find('.//diaPeptidePaths/string[1]').text) == diadir.joinpath('peptides.txt')
    assert PureWindowsPath(root.find('.//diaEvidencePaths/string[1]').text) == diadir.joinpath('evidence.txt')
    assert PureWindowsPath(root.find('.//diaMsmsPaths/string[1]').text) == diadir.joinpath('msms.txt')
    assert root.find('.//numThreads').text == '2'
    assert root.find('.//useDotNetCore').text == 'False'
    assert root.find('.//writeMzTab').text == 'True'


def test_fixparameters_windowsnofastadir(pytester):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-windows.xml')
    rawdir = PureWindowsPath('C:\\home\\poitrac\\maxquant_test')
    runner = CliRunner()
    result = runner.invoke(FixParameters.fixparameters, ['-p', parameters, '-d', str(rawdir)])
    assert result.exit_code == 0
    root = ElementTree.fromstring(result.output)
    assert PureWindowsPath(root.find('.//fastaFilePath').text) == rawdir.joinpath(
        'SwissProt_Human_txid9606_20190424.fasta')
    assert PureWindowsPath(root.find('./filePaths/string[1]').text) == rawdir.joinpath('OF_20190610_COU_01.raw')
    assert PureWindowsPath(root.find('./filePaths/string[2]').text) == rawdir.joinpath('OF_20190610_COU_02.raw')
    assert PureWindowsPath(root.find('.//diaLibraryPath/string[1]').text) == rawdir.joinpath('spectral_library.tsv')
    assert PureWindowsPath(root.find('.//diaPeptidePaths/string[1]').text) == rawdir.joinpath('peptides.txt')
    assert PureWindowsPath(root.find('.//diaEvidencePaths/string[1]').text) == rawdir.joinpath('evidence.txt')
    assert PureWindowsPath(root.find('.//diaMsmsPaths/string[1]').text) == rawdir.joinpath('msms.txt')
    assert root.find('.//numThreads').text == '2'
    assert root.find('.//useDotNetCore').text == 'False'
    assert root.find('.//writeMzTab').text == 'True'


def test_fixparameters_windowsandthreads(pytester):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-windows.xml')
    rawdir = PureWindowsPath('C:\\home\\poitrac\\maxquant_test')
    fastadir = PureWindowsPath('C:\\home\\poitrac\\fastas')
    diadir = PureWindowsPath('C:\\home\\poitrac\\dia')
    runner = CliRunner()
    result = runner.invoke(FixParameters.fixparameters,
                           ['-p', parameters, '-d', str(rawdir), '-fd', str(fastadir), '--diadir', str(diadir), '-t',
                            '4'])
    assert result.exit_code == 0
    root = ElementTree.fromstring(result.output)
    assert PureWindowsPath(root.find('.//fastaFilePath').text) == fastadir.joinpath(
        'SwissProt_Human_txid9606_20190424.fasta')
    assert PureWindowsPath(root.find('./filePaths/string[1]').text) == rawdir.joinpath('OF_20190610_COU_01.raw')
    assert PureWindowsPath(root.find('./filePaths/string[2]').text) == rawdir.joinpath('OF_20190610_COU_02.raw')
    assert PureWindowsPath(root.find('.//diaLibraryPath/string[1]').text) == diadir.joinpath('spectral_library.tsv')
    assert PureWindowsPath(root.find('.//diaPeptidePaths/string[1]').text) == diadir.joinpath('peptides.txt')
    assert PureWindowsPath(root.find('.//diaEvidencePaths/string[1]').text) == diadir.joinpath('evidence.txt')
    assert PureWindowsPath(root.find('.//diaMsmsPaths/string[1]').text) == diadir.joinpath('msms.txt')
    assert root.find('.//numThreads').text == '4'
    assert root.find('.//useDotNetCore').text == 'False'
    assert root.find('.//writeMzTab').text == 'True'


def test_fixparameters_windows2linux(pytester):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-windows.xml')
    rawdir = Path('/home/poitrac/maxquant_test')
    fastadir = Path('/home/poitrac/fastas')
    diadir = Path('/home/poitrac/dia')
    runner = CliRunner()
    result = runner.invoke(FixParameters.fixparameters,
                           ['-p', parameters, '-d', str(rawdir), '-fd', str(fastadir), '--diadir', str(diadir)])
    assert result.exit_code == 0
    root = ElementTree.fromstring(result.output)
    assert Path(root.find('.//fastaFilePath').text) == fastadir.joinpath(
        'SwissProt_Human_txid9606_20190424.fasta')
    assert Path(root.find('./filePaths/string[1]').text) == rawdir.joinpath('OF_20190610_COU_01.raw')
    assert Path(root.find('./filePaths/string[2]').text) == rawdir.joinpath('OF_20190610_COU_02.raw')
    assert Path(root.find('.//diaLibraryPath/string[1]').text) == diadir.joinpath('spectral_library.tsv')
    assert Path(root.find('.//diaPeptidePaths/string[1]').text) == diadir.joinpath('peptides.txt')
    assert Path(root.find('.//diaEvidencePaths/string[1]').text) == diadir.joinpath('evidence.txt')
    assert Path(root.find('.//diaMsmsPaths/string[1]').text) == diadir.joinpath('msms.txt')
    assert root.find('.//numThreads').text == '2'
    assert root.find('.//useDotNetCore').text == 'False'
    assert root.find('.//writeMzTab').text == 'True'


def test_fixparameters_windowskeepcore(pytester):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-windows.xml')
    rawdir = PureWindowsPath('C:\\home\\poitrac\\maxquant_test')
    fastadir = PureWindowsPath('C:\\home\\poitrac\\fastas')
    diadir = PureWindowsPath('C:\\home\\poitrac\\dia')
    runner = CliRunner()
    result = runner.invoke(FixParameters.fixparameters,
                           ['-p', parameters, '-d', str(rawdir), '-fd', str(fastadir), '--diadir', str(diadir),
                            '--keep-core'])
    assert result.exit_code == 0
    root = ElementTree.fromstring(result.output)
    assert PureWindowsPath(root.find('.//fastaFilePath').text) == fastadir.joinpath(
        'SwissProt_Human_txid9606_20190424.fasta')
    assert PureWindowsPath(root.find('./filePaths/string[1]').text) == rawdir.joinpath('OF_20190610_COU_01.raw')
    assert PureWindowsPath(root.find('./filePaths/string[2]').text) == rawdir.joinpath('OF_20190610_COU_02.raw')
    assert PureWindowsPath(root.find('.//diaLibraryPath/string[1]').text) == diadir.joinpath('spectral_library.tsv')
    assert PureWindowsPath(root.find('.//diaPeptidePaths/string[1]').text) == diadir.joinpath('peptides.txt')
    assert PureWindowsPath(root.find('.//diaEvidencePaths/string[1]').text) == diadir.joinpath('evidence.txt')
    assert PureWindowsPath(root.find('.//diaMsmsPaths/string[1]').text) == diadir.joinpath('msms.txt')
    assert root.find('.//numThreads').text == '2'
    assert root.find('.//useDotNetCore').text == 'True'
    assert root.find('.//writeMzTab').text == 'True'


def test_fixparameters_windows2linuxnofastadir(pytester):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-windows.xml')
    rawdir = Path('/home/poitrac/maxquant_test')
    runner = CliRunner()
    result = runner.invoke(FixParameters.fixparameters, ['-p', parameters, '-d', str(rawdir)])
    assert result.exit_code == 0
    root = ElementTree.fromstring(result.output)
    assert Path(root.find('.//fastaFilePath').text) == rawdir.joinpath(
        'SwissProt_Human_txid9606_20190424.fasta')
    assert Path(root.find('./filePaths/string[1]').text) == rawdir.joinpath('OF_20190610_COU_01.raw')
    assert Path(root.find('./filePaths/string[2]').text) == rawdir.joinpath('OF_20190610_COU_02.raw')
    assert Path(root.find('.//diaLibraryPath/string[1]').text) == rawdir.joinpath('spectral_library.tsv')
    assert Path(root.find('.//diaPeptidePaths/string[1]').text) == rawdir.joinpath('peptides.txt')
    assert Path(root.find('.//diaEvidencePaths/string[1]').text) == rawdir.joinpath('evidence.txt')
    assert Path(root.find('.//diaMsmsPaths/string[1]').text) == rawdir.joinpath('msms.txt')
    assert root.find('.//numThreads').text == '2'
    assert root.find('.//useDotNetCore').text == 'False'
    assert root.find('.//writeMzTab').text == 'True'


def test_fixparameters_windows2linuxandthreads(pytester):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-windows.xml')
    rawdir = Path('/home/poitrac/maxquant_test')
    fastadir = Path('/home/poitrac/fastas')
    diadir = Path('/home/poitrac/fastas')
    runner = CliRunner()
    result = runner.invoke(FixParameters.fixparameters,
                           ['-p', parameters, '-d', str(rawdir), '-fd', str(fastadir), '--diadir', str(diadir), '-t',
                            '4'])
    assert result.exit_code == 0
    root = ElementTree.fromstring(result.output)
    assert Path(root.find('.//fastaFilePath').text) == fastadir.joinpath(
        'SwissProt_Human_txid9606_20190424.fasta')
    assert Path(root.find('./filePaths/string[1]').text) == rawdir.joinpath('OF_20190610_COU_01.raw')
    assert Path(root.find('./filePaths/string[2]').text) == rawdir.joinpath('OF_20190610_COU_02.raw')
    assert Path(root.find('.//diaLibraryPath/string[1]').text) == diadir.joinpath('spectral_library.tsv')
    assert Path(root.find('.//diaPeptidePaths/string[1]').text) == diadir.joinpath('peptides.txt')
    assert Path(root.find('.//diaEvidencePaths/string[1]').text) == diadir.joinpath('evidence.txt')
    assert Path(root.find('.//diaMsmsPaths/string[1]').text) == diadir.joinpath('msms.txt')
    assert root.find('.//numThreads').text == '4'
    assert root.find('.//useDotNetCore').text == 'False'
    assert root.find('.//writeMzTab').text == 'True'


def test_fixparameters_linux(pytester):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-linux.xml')
    rawdir = Path('/home/poitrac/maxquant_test')
    fastadir = Path('/home/poitrac/fastas')
    diadir = Path('/home/poitrac/dia')
    runner = CliRunner()
    result = runner.invoke(FixParameters.fixparameters,
                           ['-p', parameters, '-d', str(rawdir), '-fd', str(fastadir), '--diadir', str(diadir)])
    assert result.exit_code == 0
    root = ElementTree.fromstring(result.output)
    assert Path(root.find('.//fastaFilePath').text) == fastadir.joinpath(
        'SwissProt_Human_txid9606_20190424.fasta')
    assert Path(root.find('./filePaths/string[1]').text) == rawdir.joinpath('OF_20190610_COU_01.raw')
    assert Path(root.find('./filePaths/string[2]').text) == rawdir.joinpath('OF_20190610_COU_02.raw')
    assert Path(root.find('.//diaLibraryPath/string[1]').text) == diadir.joinpath('spectral_library.tsv')
    assert Path(root.find('.//diaPeptidePaths/string[1]').text) == diadir.joinpath('peptides.txt')
    assert Path(root.find('.//diaEvidencePaths/string[1]').text) == diadir.joinpath('evidence.txt')
    assert Path(root.find('.//diaMsmsPaths/string[1]').text) == diadir.joinpath('msms.txt')
    assert root.find('.//numThreads').text == '2'
    assert root.find('.//useDotNetCore').text == 'False'
    assert root.find('.//writeMzTab').text == 'True'


def test_fixparameters_linuxnofastadir(pytester):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-linux.xml')
    rawdir = Path('/home/poitrac/maxquant_test')
    runner = CliRunner()
    result = runner.invoke(FixParameters.fixparameters, ['-p', parameters, '-d', str(rawdir)])
    assert result.exit_code == 0
    root = ElementTree.fromstring(result.output)
    assert Path(root.find('.//fastaFilePath').text) == rawdir.joinpath(
        'SwissProt_Human_txid9606_20190424.fasta')
    assert Path(root.find('./filePaths/string[1]').text) == rawdir.joinpath('OF_20190610_COU_01.raw')
    assert Path(root.find('./filePaths/string[2]').text) == rawdir.joinpath('OF_20190610_COU_02.raw')
    assert Path(root.find('.//diaLibraryPath/string[1]').text) == rawdir.joinpath('spectral_library.tsv')
    assert Path(root.find('.//diaPeptidePaths/string[1]').text) == rawdir.joinpath('peptides.txt')
    assert Path(root.find('.//diaEvidencePaths/string[1]').text) == rawdir.joinpath('evidence.txt')
    assert Path(root.find('.//diaMsmsPaths/string[1]').text) == rawdir.joinpath('msms.txt')
    assert root.find('.//numThreads').text == '2'
    assert root.find('.//useDotNetCore').text == 'False'
    assert root.find('.//writeMzTab').text == 'True'


def test_fixparameters_linuxandthreads(pytester):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-linux.xml')
    rawdir = Path('/home/poitrac/maxquant_test')
    fastadir = Path('/home/poitrac/fastas')
    diadir = Path('/home/poitrac/dia')
    runner = CliRunner()
    result = runner.invoke(FixParameters.fixparameters,
                           ['-p', parameters, '-d', str(rawdir), '-fd', str(fastadir), '--diadir', str(diadir), '-t',
                            '4'])
    assert result.exit_code == 0
    root = ElementTree.fromstring(result.output)
    assert Path(root.find('.//fastaFilePath').text) == fastadir.joinpath(
        'SwissProt_Human_txid9606_20190424.fasta')
    assert Path(root.find('./filePaths/string[1]').text) == rawdir.joinpath('OF_20190610_COU_01.raw')
    assert Path(root.find('./filePaths/string[2]').text) == rawdir.joinpath('OF_20190610_COU_02.raw')
    assert Path(root.find('.//diaLibraryPath/string[1]').text) == diadir.joinpath('spectral_library.tsv')
    assert Path(root.find('.//diaPeptidePaths/string[1]').text) == diadir.joinpath('peptides.txt')
    assert Path(root.find('.//diaEvidencePaths/string[1]').text) == diadir.joinpath('evidence.txt')
    assert Path(root.find('.//diaMsmsPaths/string[1]').text) == diadir.joinpath('msms.txt')
    assert root.find('.//numThreads').text == '4'
    assert root.find('.//useDotNetCore').text == 'False'
    assert root.find('.//writeMzTab').text == 'True'


def test_fixparameters_linux2windowds(pytester):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-linux.xml')
    rawdir = PureWindowsPath('C:\\home\\poitrac\\maxquant_test')
    fastadir = PureWindowsPath('C:\\home\\poitrac\\fastas')
    diadir = PureWindowsPath('C:\\home\\poitrac\\dia')
    runner = CliRunner()
    result = runner.invoke(FixParameters.fixparameters,
                           ['-p', parameters, '-d', str(rawdir), '-fd', str(fastadir), '--diadir', str(diadir)])
    assert result.exit_code == 0
    root = ElementTree.fromstring(result.output)
    assert PureWindowsPath(root.find('.//fastaFilePath').text) == fastadir.joinpath(
        'SwissProt_Human_txid9606_20190424.fasta')
    assert PureWindowsPath(root.find('./filePaths/string[1]').text) == rawdir.joinpath('OF_20190610_COU_01.raw')
    assert PureWindowsPath(root.find('./filePaths/string[2]').text) == rawdir.joinpath('OF_20190610_COU_02.raw')
    assert PureWindowsPath(root.find('.//diaLibraryPath/string[1]').text) == diadir.joinpath('spectral_library.tsv')
    assert PureWindowsPath(root.find('.//diaPeptidePaths/string[1]').text) == diadir.joinpath('peptides.txt')
    assert PureWindowsPath(root.find('.//diaEvidencePaths/string[1]').text) == diadir.joinpath('evidence.txt')
    assert PureWindowsPath(root.find('.//diaMsmsPaths/string[1]').text) == diadir.joinpath('msms.txt')
    assert root.find('.//numThreads').text == '2'
    assert root.find('.//useDotNetCore').text == 'False'
    assert root.find('.//writeMzTab').text == 'True'


def test_fixparameters_linux2windowdsnofastadir(pytester):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-linux.xml')
    rawdir = PureWindowsPath('C:\\home\\poitrac\\maxquant_test')
    runner = CliRunner()
    result = runner.invoke(FixParameters.fixparameters, ['-p', parameters, '-d', str(rawdir)])
    assert result.exit_code == 0
    root = ElementTree.fromstring(result.output)
    assert PureWindowsPath(root.find('.//fastaFilePath').text) == rawdir.joinpath(
        'SwissProt_Human_txid9606_20190424.fasta')
    assert PureWindowsPath(root.find('./filePaths/string[1]').text) == rawdir.joinpath('OF_20190610_COU_01.raw')
    assert PureWindowsPath(root.find('./filePaths/string[2]').text) == rawdir.joinpath('OF_20190610_COU_02.raw')
    assert PureWindowsPath(root.find('.//diaLibraryPath/string[1]').text) == rawdir.joinpath('spectral_library.tsv')
    assert PureWindowsPath(root.find('.//diaPeptidePaths/string[1]').text) == rawdir.joinpath('peptides.txt')
    assert PureWindowsPath(root.find('.//diaEvidencePaths/string[1]').text) == rawdir.joinpath('evidence.txt')
    assert PureWindowsPath(root.find('.//diaMsmsPaths/string[1]').text) == rawdir.joinpath('msms.txt')
    assert root.find('.//numThreads').text == '2'
    assert root.find('.//useDotNetCore').text == 'False'
    assert root.find('.//writeMzTab').text == 'True'


def test_fixparameters_linux2windowdsandthreads(pytester):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-linux.xml')
    rawdir = PureWindowsPath('C:\\home\\poitrac\\maxquant_test')
    fastadir = PureWindowsPath('C:\\home\\poitrac\\fastas')
    diadir = PureWindowsPath('C:\\home\\poitrac\\dia')
    runner = CliRunner()
    result = runner.invoke(FixParameters.fixparameters,
                           ['-p', parameters, '-d', str(rawdir), '-fd', str(fastadir), '--diadir', str(diadir), '-t',
                            '4'])
    assert result.exit_code == 0
    root = ElementTree.fromstring(result.output)
    assert PureWindowsPath(root.find('.//fastaFilePath').text) == fastadir.joinpath(
        'SwissProt_Human_txid9606_20190424.fasta')
    assert PureWindowsPath(root.find('./filePaths/string[1]').text) == rawdir.joinpath('OF_20190610_COU_01.raw')
    assert PureWindowsPath(root.find('./filePaths/string[2]').text) == rawdir.joinpath('OF_20190610_COU_02.raw')
    assert PureWindowsPath(root.find('.//diaLibraryPath/string[1]').text) == diadir.joinpath('spectral_library.tsv')
    assert PureWindowsPath(root.find('.//diaPeptidePaths/string[1]').text) == diadir.joinpath('peptides.txt')
    assert PureWindowsPath(root.find('.//diaEvidencePaths/string[1]').text) == diadir.joinpath('evidence.txt')
    assert PureWindowsPath(root.find('.//diaMsmsPaths/string[1]').text) == diadir.joinpath('msms.txt')
    assert root.find('.//numThreads').text == '4'
    assert root.find('.//useDotNetCore').text == 'False'
    assert root.find('.//writeMzTab').text == 'True'


def test_fixparameters_linux_160(pytester):
    parent = Path(__file__).parent
    parameters = parent.joinpath('mqpar-linux-1.6.0.xml')
    rawdir = Path('/home/poitrac/maxquant_test')
    fastadir = Path('/home/poitrac/fastas')
    diadir = Path('/home/poitrac/dia')
    runner = CliRunner()
    result = runner.invoke(FixParameters.fixparameters,
                           ['-p', parameters, '-d', str(rawdir), '-fd', str(fastadir), '--diadir', str(diadir)])
    assert result.exit_code == 0
    root = ElementTree.fromstring(result.output)
    assert Path(root.find('.//fastaFiles/string[1]').text) == fastadir.joinpath(
        'SwissProt_Human_txid9606_20190424.fasta')
    assert Path(root.find('./filePaths/string[1]').text) == rawdir.joinpath('OF_20190610_COU_01.raw')
    assert Path(root.find('./filePaths/string[2]').text) == rawdir.joinpath('OF_20190610_COU_02.raw')
    assert Path(root.find('.//diaLibraryPath/string[1]').text) == diadir.joinpath('spectral_library.tsv')
    assert Path(root.find('.//diaPeptidePaths/string[1]').text) == diadir.joinpath('peptides.txt')
    assert Path(root.find('.//diaEvidencePaths/string[1]').text) == diadir.joinpath('evidence.txt')
    assert Path(root.find('.//diaMsmsPaths/string[1]').text) == diadir.joinpath('msms.txt')
    assert root.find('.//numThreads').text == '2'
    assert root.find('.//useDotNetCore').text == 'False'
    assert root.find('.//writeMzTab').text == 'True'
