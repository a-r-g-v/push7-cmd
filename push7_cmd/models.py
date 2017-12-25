# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

from push7_cmd import get_logger
from push7_cmd.exceptions import (NotFoundApplicationException, FailedToAuthorizationException,
        Push7ServerErrorException, Push7CmdBaseException)


class StateStore(object):
    DEFAULT_PERSISTENT_STORE = '~/.push7-cmd/'

    def save_application(self, application):
        return None

    def list_applications(self):
        return []

    def delete_application(self, appno):
        return False

    def get_default_application(self):
        return None

    def save_default_application(self, appno):
        return False



class Push7Sendable(object):

    def __init__(self, client):
        self._client = client

    def send(self):
        from push7.exceptions import (
                NotFoundException, Push7BaseException, 
                ForbiddenException, UnauthorizedException,
                ServerErrorException
                )
        try:
            self._client.push(self._title, self._body, self._icon, self._url).send()
        except NotFoundException as e:
            get_logger().error.exception("Sendable Client Error", e)
            raise NotFoundApplicationException(self._client.appno)
        except (ForbiddenException, UnauthorizedException) as e:
            get_logger().error.exception("Sendable Client Error", e)
            raise FailedToAuthorizationException(self._client.appno)
        except ServerErrorException as e:
            get_logger().error.exception("Sendable Server Error", e)
            raise Push7ServerErrorException(e)
        except Push7BaseException as e:
            get_logger().critical.exception("Sendable Library Error", e)
            raise Push7CmdBaseException(e)



class Push(Push7Sendable):
    def __init__(self, client, title, body, icon, url, disappear=None):
        """
            Note: Currently, we do not support disappear push.
        """
        super(Push7Sendable, self).__init__(client)

        if disappear:
            import warning
            warning.warn('The options about disappear of push has ignored.')

        self._title = title
        self._body = body
        self._icon = icon
        self._url = url
        self._disappear = None

class Application(object):
    DEFAULT_TITLE = "Push7-Cmd"
    DEFAULT_URL = "https://push7.jp"
    DEFAULT_ICON = "https://push7.jp/assets/images/push7_logo.svg"
    PUSH_CLS = Push

    def __init__(self, appno, apikey):
        from push7 import Client
        self._appno = appno
        self._client = Client(appno, apikey)

    @property
    def icon(self):
        return self.DEFAULT_ICON

    @property
    def url(self):
        return self.URL

    def create_push(self, body, title=None, icon=None, url=None, disappear=None):

        if not title:
            title = self.DEFAULT_TITLE

        if not icon:
            icon = self.DEFAULT_ICON

        if not url:
            url = self.DEFAULT_URL


        return self.PUSH_CLS(self._client, title, body, icon, url, disappear=disappear)

class Interactor(object):
    APPLICATION_CLS = Application
    STATE_STORE_CLS = StateStore

    def __init__(self, logger_name=None):
        self._store = self.STATE_STORE_CLS()
        self._logger = get_logger(logger_name)

    def create_application(self, appno, apikey):
        new_application = Application(appno, apikey)
        self._store.save_application(new_application)

    def list_application(self):
        return self._store.list_applications()

    def delete_application(self, appno):
        self._store.delete_application(appno)

    def set_default_application(self, appno):
        self._store.save_default_application(appno)

    def create_push_using_default_application(self, body, title=None):
        application = self._store.get_default_application()
        push = application.create_push(body)
        push.send()

    @property
    def logger(self):
        return self._logger
