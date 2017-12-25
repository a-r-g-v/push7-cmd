# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

from push7_cmd import get_logger, add_handler
from push7_cmd.exceptions import (NotFoundApplicationException, FailedToAuthorizationException,
        Push7ServerErrorException, Push7CmdBaseException, NotFoundDefaultApplicationException,
        NotFoundRegistedApplicationException)
from os.path import expanduser
import six

class State(object):

    STATE_STORE_FILE_PATH = 'config'
    STATE_STORE_DIR_PATH = expanduser("~/.push7-cmd/")
    STATE_STORE_PATH = STATE_STORE_DIR_PATH + STATE_STORE_FILE_PATH

    def __init__(self):
        self.applications = {}
        self.default_appno = None

    def save(self):
        with open(self.STATE_STORE_PATH, mode='wb') as f:
            import pickle
            pickle.dump(self, f)

    @classmethod
    def restore(cls):
        obj = None
        with open(cls.STATE_STORE_PATH, mode='rb') as f:
            import pickle
            obj = pickle.load(f)

        if isinstance(obj, cls):
            return obj

        import os
        os.remove(cls.STATE_STORE_PATH)
        get_logger().critical('A restored state object from PATH is not instance of State class. This command removed the PATH and created new ones.')
        return cls.new()


    @classmethod
    def new(cls):
        import os, os.path
        try:
            os.makedirs(cls.STATE_STORE_DIR_PATH)
        except OSError as e:
            if not os.path.isdir(cls.STATE_STORE_DIR_PATH):
                raise

        return cls()

    @classmethod
    def new_or_restore(cls):
        import os.path
        if os.path.exists(cls.STATE_STORE_PATH):
            return cls.restore()

        return cls.new()

class Repository(object):
    STATE_CLS = State

    def save_application(self, application):
        self._store = State.new_or_restore()
        self._store.applications.update({application.appno : application})
        self._store.save()

    def list_applications(self):
        self._store = State.new_or_restore()
        return six.itervalues(self._store.applications)

    def delete_application(self, appno):
        self._store = State.new_or_restore()
        try:
            self._store.applications.pop(appno)
        except IndexError:
            raise NotFoundRegistedApplicationException(appno)
        finally:
            self._store.save()

    def get_default_application(self):
        self._store = State.new_or_restore()
        application = self._store.applications.get(self._store.default_appno, None)
        if not application:
            raise NotFoundDefaultApplicationException()
        return application

    def save_default_application(self, appno):
        self._store = State.new_or_restore()
        self._store.default_appno = appno
        self._store.save()


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
        super(Push, self).__init__(client)

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

    @property
    def appno(self):
        return self._appno

    def __eq__(self, other):
        return self.appno == other.appno

class Interactor(object):
    APPLICATION_CLS = Application
    STORE_CLS = Repository

    def __init__(self, is_debug=False, logger_name=None):
        import logging
        self._store = self.STORE_CLS()
        self._logger = get_logger(logger_name)

        logger_level = logging.INFO if not is_debug else logging.DEBUG
        add_handler(self._logger, level=logger_level)

    def create_application(self, appno, apikey):
        new_application = Application(appno, apikey)
        self._store.save_application(new_application)

    def list_applications(self):
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
