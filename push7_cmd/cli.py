# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import click
from six.moves import input
from click_default_group import DefaultGroup

from push7_cmd.models import Interactor


@click.group()
def applications():
    pass

@applications.command()
@click.argument('appno')
@click.argument('apikey')
@click.pass_context
def add(ctx, appno, apikey):
    ctx.obj.logger.debug("incoming appno : %s apikey : %s " % (str(appno), str(apikey)) )
    ctx.obj.create_application(appno, apikey)
    print('added the app(appno:%s)' % (str(appno), ))
    ctx.obj.set_default_application(appno)
    print('set the app(appno:%s) as default application ' % (str(appno), ))

@applications.command()
@click.pass_context
def list(ctx):
    print('appno')
    for application in ctx.obj.list_applications():
        print('%s' % application.appno)

@applications.command()
@click.argument('appno')
@click.pass_context
def use(ctx, appno):
    ctx.obj.logger.debug("incoming appno : %s " % (str(appno),) )
    ctx.obj.set_default_application(appno)
    print('set the app(appno:%s) as default application ' % (str(appno), ))

@applications.command()
@click.argument('appno')
@click.pass_context
def delete(ctx, appno):
    ctx.obj.logger.debug("incoming appno : %s " % (str(appno),) )
    ctx.obj.delete_application(appno)

@click.group(cls=DefaultGroup, default='main', default_if_no_args=True)
@click.option('--debug', is_flag=True, default=False)
@click.pass_context
def cli(ctx, debug):
    ctx.obj = Interactor(is_debug=debug)

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
    cli()

if __name__ == '__main__':
    invoke()
