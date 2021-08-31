import os
import subprocess
from xml.etree import ElementTree

import click

from maxquanttools import FixParameters


@click.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.option('--parameters', type=click.Path(exists=True), default='mqpar.xml', show_default=True,
              help='MaxQuant parameter file.')
@click.option('--rawdir', type=click.Path(),
              help='Directory to use for RAW and FASTA files. Defaults to working directory.')
@click.option('--max-threads', type=int, default=40, show_default=True,
              help='Maximum number of CPUs for SBATCH.')
@click.option('--max-mem', type=int, default=185, show_default=True,
              help='Maximum amount of memory for SBATCH in gigabytes.')
@click.option('--mail', envvar='JOB_MAIL', required=True,
              help='Email address for notification.')
@click.option('--parameters-output', type=click.Path(), default='mqpar-run.xml', show_default=True,
              help='Where to write modified file. Defaults to mqpar-run.xml.')
@click.argument('maxquant_args', nargs=-1, type=click.UNPROCESSED)
def maxquant(parameters, rawdir, max_threads, max_mem, maxquant_args, mail, parameters_output):
    """Fixes parameter file and starts MaxQuant using sbatch."""
    tree = ElementTree.parse(parameters)
    root = tree.getroot()
    samples = len(root.findall('./filePaths/string'))
    threads = min(samples, max_threads)  # One thread per sample
    mem = min(samples * 5, max_mem)  # 5GB of memory per samples
    mem = max(mem, 6)  # Minimum of 6GB of memory
    if not rawdir:
        rawdir = os.getcwd()
    FixParameters.fixparameters_(parameters, rawdir=rawdir, threads=threads, output=parameters_output)
    cmd = ['sbatch', '--cpus-per-task=' + str(threads), '--mem=' + str(mem) + 'G', '--mail-type=ALL',
           '--mail-user=' + mail, 'maxquantcmd-mono.sh'] + list(maxquant_args) + [str(parameters_output)]
    subprocess.run(cmd, check=True)


if __name__ == '__main__':
    maxquant()
