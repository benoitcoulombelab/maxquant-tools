import os
import subprocess
import logging

import click
import yaml

from maxquanttools import FixParameters


def validate_mail(ctx, param, value):
    """Validates that mail is supplied"""
    send_mail = ctx.params['send_mail'] if 'send_mail' in ctx.params else True
    if send_mail and not value:
        raise click.BadParameter('No email address in \'JOB_MAIL\' environment variable, use --mail parameter instead')
    else:
        return value


@click.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.option('--parameters', type=click.Path(exists=True), default='mqpar.xml', show_default=True,
              help='MaxQuant parameter file.')
@click.option('--rawdir', type=click.Path(),
              help='Directory to use for RAW and FASTA files. Defaults to working directory.')
@click.option('--send-mail/--ignore-mail', default=True,
              help='Send email notifications.')
@click.option('--mail', envvar='JOB_MAIL', callback=validate_mail,
              help='Email address for notifications.')
@click.option('--parameters-output', type=click.Path(), default='mqpar-run.xml', show_default=True,
              help='Where to write modified file. Defaults to mqpar-run.xml.')
@click.option('--dryrun', '-n', is_flag=True,
              help='Print job ids and job names table.')
@click.argument('maxquant_args', nargs=-1, type=click.UNPROCESSED)
def maxquant(parameters, rawdir, maxquant_args, send_mail, mail, parameters_output, dryrun):
    """Fixes parameter file and starts MaxQuant using sbatch."""
    logging.basicConfig(filename='maxquant-tools.log', level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    config = {'threads': 24, 'memory': 120}
    user_config = 'maxquant.yml'
    if 'CC_CLUSTER' in os.environ:
        base_config = os.path.abspath(os.path.dirname(__file__)) + '/' + os.environ['CC_CLUSTER'] + '.yml'
        if os.path.exists(base_config):
            logging.debug('loading config file {}'.format(base_config))
            with open(base_config) as input:
                config = yaml.safe_load(input)
    if os.path.exists(user_config):
        logging.debug('loading config file {}'.format(user_config))
        with open(user_config) as input:
            config = yaml.safe_load(input)
    logging.debug('config is {}'.format(config))
    threads = max(config['threads'], 1)  # At least one thread
    mem = max(config['memory'], 6)  # Minimum of 6GB of memory
    if not rawdir:
        rawdir = os.getcwd()
    FixParameters.fixparameters_(parameters, rawdir=rawdir, threads=threads, output=parameters_output)
    cmd = []
    if not dryrun:
        cmd.extend(['sbatch', '--cpus-per-task=' + str(threads), '--mem=' + str(mem) + 'G'])
        if send_mail:
            cmd.extend(['--mail-type=ALL', '--mail-user=' + mail])
    cmd.append('maxquantcmd-mono.sh')
    if dryrun:
        cmd.append('-n')
    cmd.extend(list(maxquant_args))
    cmd.append(str(parameters_output))
    subprocess.run(cmd, check=True)


if __name__ == '__main__':
    maxquant()
