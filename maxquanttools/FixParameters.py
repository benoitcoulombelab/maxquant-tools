import os
from pathlib import Path, PureWindowsPath
from xml.etree import ElementTree

import click
import sys


@click.command()
@click.option('--parameters', '-p', type=click.Path(exists=True), default='mqpar.xml', show_default=True,
              help='MaxQuant parameter file.')
@click.option('--rawdir', '-d', type=click.Path(),
              help='Directory to use for RAW files. Defaults to not changing parameter file.')
@click.option('--fastadir', '-fd', type=click.Path(),
              help='Directory to use for fasta file. Defaults to the same as --rawdir if defined,' +
                   ' otherwise does not change parameter file.')
@click.option('--diadir', type=click.Path(),
              help='Directory to use for DIA library/discovery files. Defaults to the same as --rawdir if defined,' +
                   ' otherwise does not change parameter file.')
@click.option('--threads', '-t', type=int,
              help='Numbers of threads to use. Defaults to not changing parameter file.')
@click.option('--disable-core/--keep-core', default=True, show_default=True,
              help='Disables .NET core requirement. Must be True for Linux.')
@click.option('--output', '-o', type=click.Path(),
              help='Where to write modified file. Defaults to standard output.')
def fixparameters(parameters, rawdir, fastadir, diadir, threads, disable_core, output):
    """Fixes MaxQuant parameters by replacing directories and fixing threads."""
    fixparameters_(parameters, rawdir, fastadir, diadir, threads, disable_core, output)


def fixparameters_(parameters='mqpar.xml', rawdir=None, fastadir=None, diadir=None, threads=None, disable_core=True,
                   output=None):
    """Fixes MaxQuant parameters by replacing directories and fixing threads."""
    if not fastadir and rawdir:
        fastadir = rawdir
    if not diadir and rawdir:
        diadir = rawdir
    if not output:
        output = sys.stdout
    tree = ElementTree.parse(parameters)
    root = tree.getroot()
    if fastadir:
        fastas = root.findall('.//fastaFilePath')
        # Older MaxQuant versions
        fastas.extend(root.findall('.//fastaFiles/string'))
        for fasta_file_path in fastas:
            fasta = update_dir(fasta_file_path.text.strip(), fastadir)
            if fasta != fasta_file_path.text:
                fasta_file_path.text = fasta
    if rawdir:
        for file in root.findall('./filePaths/string'):
            f = update_dir(file.text.strip(), rawdir)
            if f != file.text:
                file.text = f
    if diadir:
        for file in root.findall('.//diaLibraryPath/string'):
            f = update_dir(file.text.strip(), diadir)
            if f != file.text:
                file.text = f
        for file in root.findall('.//diaPeptidePaths/string'):
            f = update_dir(file.text.strip(), diadir)
            if f != file.text:
                file.text = f
        for file in root.findall('.//diaEvidencePaths/string'):
            f = update_dir(file.text.strip(), diadir)
            if f != file.text:
                file.text = f
        for file in root.findall('.//diaMsmsPaths/string'):
            f = update_dir(file.text.strip(), diadir)
            if f != file.text:
                file.text = f
    if threads:
        num_threads = root.find('.//numThreads')
        if str(threads) != num_threads.text:
            num_threads.text = str(threads)
    if disable_core:
        for use_dot_net_core in root.findall('.//useDotNetCore'):
            use_dot_net_core.text = 'False'
    # Force writing mzTab output file.
    for write_mz_tab in root.findall('.//writeMzTab'):
        write_mz_tab.text = 'True'
    tree.write(output, encoding='unicode', xml_declaration=True, short_empty_elements=False)


def update_dir(file, directory):
    """Updates file's directory with directory."""
    file = create_path(file)
    if not path_is_abs(directory):
        directory = os.path.abspath(directory)
    directory = create_path(directory)
    return str(directory.joinpath(file.name))


def create_path(path):
    """Creates a Path from path with support for Windows."""
    if '\\' in path:
        return PureWindowsPath(path)
    else:
        return Path(path)


def path_is_abs(p): return (len(p) > 0 and p[0] == '/') or (len(p) > 1 and p[1] == ':')


if __name__ == '__main__':
    fixparameters()
