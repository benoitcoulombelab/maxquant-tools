import sys
from pathlib import Path, PureWindowsPath
from xml.etree import ElementTree

import click


@click.command()
@click.option('--parameters', '-p', type=click.Path(exists=True), default='mqpar.xml', show_default=True,
              help='MaxQuant parameter file.')
@click.option('--rawdir', '-d', type=click.Path(),
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
def fixparameters(parameters, rawdir, fastadir, threads, disable_core, output):
    """Fixes MaxQuant parameters by replacing directories and fixing threads."""
    if not fastadir and rawdir:
        fastadir = rawdir
    if not output:
        output = sys.stdout
    tree = ElementTree.parse(parameters)
    root = tree.getroot()
    if fastadir:
        for fasta_file_path in root.findall('.//fastaFilePath'):
            fasta = update_dir(fasta_file_path.text, fastadir)
            if fasta != fasta_file_path.text:
                fasta_file_path.text = fasta
    if rawdir:
        for file in root.findall('./filePaths/string'):
            f = update_dir(file.text, rawdir)
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
    directory = create_path(directory)
    return str(directory.joinpath(file.name))


def create_path(path):
    """Creates a Path from path with support for Windows."""
    if '\\' in path:
        return PureWindowsPath(path)
    else:
        return Path(path)


if __name__ == '__main__':
    fixparameters()
