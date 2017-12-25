# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
from click import ClickException

class Push7CmdBaseException(ClickException):

    exit_code = 64
    exit_message = "An unknown error occurred. Please report this problem with above stacktraces (issues management: https://github.com/a-r-g-v/push7-cmd/issues/new )."

    def __init__(self):
        super(Push7CmdBaseException, self).__init__(self.exit_message)

class NotFoundApplicationException(Push7CmdBaseException):
    exit_code = 65
    exit_message = "The application was not found in push7. Please change the default application from this to valid ones."


class FailedToAuthorizationException(Push7CmdBaseException):
    exit_code = 66
    exit_message = "This command failed by authorization error. Please change the default application from this to valid ones."

class Push7ServerErrorException(Push7CmdBaseException):
    exit_code = 67
    exit_message = "This command failed by unknown error which push7 caused. Please retry it."

class NotFoundDefaultApplicationException(Push7CmdBaseException):
    exit_code = 68
    exit_message = "This command has not any application. First, please add a application into this command."

class NotFoundRegistedApplicationException(Push7CmdBaseException):
    exit_code = 69
    exit_message = "An application was not found which has the given appno."
