# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import click
from six.moves import input
from click_default_group import DefaultGroup

from push7_cmd.models import Interactor
#from push7_cmd.exceptions import Push7CmdBaseException


@click.group()
def applications():
    pass

@applications.command()
@click.argument('appno')
@click.argument('apikey')
@click.pass_context
def add(ctx, appno, apikey):
    ctx.obj.logger.debug("incoming appno : %s apikey : %s " % (str(appno), str(apikey)) )
    ctx.obj.add_application(appno, apikey)

@applications.command()
@click.pass_context
def list(ctx):
    ctx.obj.list_applications()

@applications.command()
@click.argument('appno')
@click.pass_context
def use(ctx, appno):
    ctx.obj.logger.debug("incoming appno : %s " % (str(appno),) )
    ctx.obj.set_default_application(appno)

@applications.command()
@click.argument('appno')
@click.pass_context
def delete(ctx, appno):
    ctx.obj.logger.debug("incoming appno : %s " % (str(appno),) )
    ctx.obj.delete_application(appno)

@click.group(cls=DefaultGroup, default='main', default_if_no_args=True)
@click.pass_context
def cli(ctx):
    pass

@click.option('--title', '-t', default=None)
@click.option('--body', '-b', default=None)
@cli.command()
@click.pass_context
def main(ctx, title, body):
    if not body:
        body = input()

    ctx.obj.logger.debug("incoming body: %s title : %s " % (str(body), str(title),) )
    ctx.obj.create_push_using_default_application(body, title=title)


cli.add_command(applications)

def invoke():
    intractor = Interactor()
    cli(obj=intractor)

if __name__ == '__main__':
    invoke()
