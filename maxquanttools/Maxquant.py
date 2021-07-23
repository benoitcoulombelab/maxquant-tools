import subprocess
from xml.etree import ElementTree

import click


@click.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.option('--parameters', '-p', type=click.Path(exists=True), default='mqpar.xml', show_default=True,
              help='MaxQuant parameter file.')
@click.option('--max-cpu', '-c', type=int, default=40, show_default=True,
              help='Maximum number of CPUs for SBATCH.')
@click.option('--max-mem', '-m', type=int, default=185, show_default=True,
              help='Maximum amount of memory for SBATCH in gigabytes.')
@click.option('--mail', envvar='JOB_MAIL', required=True,
              help='Email address for notification.')
@click.argument('maxquant_args', nargs=-1, type=click.UNPROCESSED)
def maxquant(parameters, max_cpu, max_mem, maxquant_args, mail):
    """Fixes parameter file and starts MaxQuant using sbatch."""
    tree = ElementTree.parse(parameters)
    root = tree.getroot()
    samples = len(root.findall('./filePaths/string'))
    threads = min(samples, max_cpu)  # One CPU per sample
    mem = min(samples * 5, max_mem)  # 5GB of memory per samples
    mem = max(mem, 6)  # Minimum of 6GB of memory
    cmd = ['sbatch', '--cpus-per-task=' + str(threads), '--mem=' + str(mem) + 'G', '--mail-type=ALL',
           '--mail-user=' + mail, 'maxquant.sh', '-p', str(parameters)] + list(maxquant_args)
    subprocess.run(cmd, check=True)


if __name__ == '__main__':
    maxquant()
