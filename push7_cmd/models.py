
class PersistentErrorException(Exception):
    pass

class StateStore(object):
    DEFAULT_PERSISTENT_STORE = '~/.push7-cmd/'

    def add_application(self, application):
        return None

    def list_applications(self):
        return []

    def delete_application(self, appno):
        return False

    def get_default_application(self):
        return None

    def set_default_application(self, appno):
        return False



class Push7Sendable(object):

    def send(self):
        pass



class Push(Push7Sendable):
    def __init__(self, title, body, icon, url, disappear=None, client=None):
        """
            Note: Currently, we do not support disappear push.
        """

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

    def create_push(self, body, title=None, icon=None, url=None, disappear=None, client=None):

        if not title:
            title = self.DEFAULT_TITLE

        if not icon:
            icon = self.DEFAULT_ICON

        if not url:
            url = self.DEFAULT_URL


        return self.PUSH_CLS(title, body, icon, url, disappear=disappear, client=client)

class Interactor(object):
    APPLICATION_CLS = Application
    STATE_STORE_CLS = StateStore
    LOGGER_NAME = "push7_cmd"

    def __init__(self):
        from logging import getLogger
        self._store = self.STATE_STORE_CLS()
        self._logger = getLogger('push7_cmd')

    def create_application(self, appno, apikey):
        new_application = Application(appno, apikey)
        self._store.save_application(new_application)
        self._store.set_default_application(new_application)
        return new_application

    def list_application(self):
        return self._store.list_applications()

    def delete_application(self, appno):
        return self._store.delete_application(appno)

    def set_default_application(self, appno):
        return self._store.set_default_application(appno)

    def create_push_using_default_application(self, body, title=None):
        application = self._store.get_default_application()
        push = application.create_push(body)
        push.send()

    @property
    def logger(self):
        return self._logger
