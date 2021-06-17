import sys
import xml.etree.ElementTree as eTree
from pathlib import Path, PureWindowsPath

import click


@click.command()
@click.option('--parameters', '-p', type=click.Path(exists=True), default='mqpar.xml', show_default=True,
              help='MaxQuant parameter file.')
@click.option('--dir', '-d', type=click.Path(),
              help='Directory to use for RAW files. Defaults to not changing parameter file.')
@click.option('--fastadir', '-fd', type=click.Path(),
              help='Directory to use for fasta file. Defaults to the same as --dir if defined,' +
                   ' otherwise does not change parameter file.')
@click.option('--threads', '-t', type=int,
              help='Numbers of threads to use. Defaults to not changing parameter file.')
@click.option('--disable-core/--keep-core', default=True, show_default=True,
              help='Disables .NET core requirement. Must be True for Linux.')
@click.option('--output', '-o', type=click.Path(),
              help='Where to write modified file. Defaults to standard output.')
def fixparameters(parameters, dir, fastadir, threads, disable_core, output):
    """Fixes MaxQuant parameters by replacing directories and fixing threads."""
    if not fastadir and dir:
        fastadir = dir
    if not output:
        output = sys.stdout
    tree = eTree.parse(parameters)
    root = tree.getroot()
    if fastadir:
        for fasta_file_path in root.findall('.//fastaFilePath'):
            fasta = update_dir(fasta_file_path.text, fastadir)
            if fasta != fasta_file_path.text:
                fasta_file_path.text = fasta
    if dir:
        for file in root.findall('./filePaths/string'):
            f = update_dir(file.text, dir)
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


def update_dir(file, dir):
    """Updates file's directory with dir."""
    file = create_path(file)
    dir = create_path(dir)
    return str(dir.joinpath(file.name))


def create_path(path):
    """Creates a Path from path with support for Windows."""
    if '\\' in path:
        return PureWindowsPath(path)
    else:
        return Path(path)


if __name__ == '__main__':
    fixparameters()
