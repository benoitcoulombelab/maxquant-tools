from pathlib import Path, PureWindowsPath
import sys

import click
import xml.etree.ElementTree as ET


@click.command()
@click.option('--parameters', '-p', type=click.Path(exists=True), default='mqpar.xml', show_default=True,
              help='MaxQuant parameter file.')
@click.option('--dir', '-d', type=click.Path(),
              help='Directory to use for RAW files. Defaults to not changing parameter file.')
@click.option('--fastadir', '-fd', type=click.Path(),
              help='Directory to use for fasta file. Defaults to the same as --dir if defined, otherwise does not change parameter file.')
@click.option('--threads', '-t', type=int,
              help='Numbers of threads to use. Defaults to not changing parameter file.')
@click.option('--disable-core/--keep-core', default=True, show_default=True,
              help='Disables .NET core requirement. Must be True for Linux.')
@click.option('--output', '-o', type=click.Path(),
              help='Where to write modified file. Defaults to standard output.')
def replacedirectories(parameters, dir, fastadir, threads, disable_core, output):
    '''Replaces directories and threads in MaxQuant parameter file.'''
    if not fastadir and dir:
        fastadir = dir
    if not output:
        output = sys.stdout
    tree = ET.parse(parameters)
    root = tree.getroot()
    if fastadir:
        for fastaFilePath in root.findall('.//fastaFilePath'):
            fasta = update_dir(fastaFilePath.text, fastadir)
            if fasta != fastaFilePath.text:
                fastaFilePath.text = fasta
    if dir:
        for file in root.findall('./filePaths/string'):
            f = update_dir(file.text, dir)
            if f != file.text:
                file.text = f
    if threads:
        numThreads = root.find('.//numThreads')
        if str(threads) != numThreads.text:
            numThreads.text = str(threads)
    if disable_core:
        for useDotNetCore in root.findall('.//useDotNetCore'):
            useDotNetCore.text = 'False'
    # Force writing mzTab output file.
    for writeMzTab in root.findall('.//writeMzTab'):
        writeMzTab.text = 'True'
    tree.write(output, encoding='unicode', xml_declaration=True, short_empty_elements=False)


def update_dir(file, dir):
    '''Updates file's directory with dir.'''
    file = create_path(file)
    dir = create_path(dir)
    return str(dir.joinpath(file.name))


def create_path(path):
    '''Creates a Path from path with support for Windows.'''
    if '\\' in path:
        return PureWindowsPath(path)
    else:
        return Path(path)


if __name__ == '__main__':
    replacedirectories()
