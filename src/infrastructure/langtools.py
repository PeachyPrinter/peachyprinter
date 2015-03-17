from os.path import join, dirname
import gettext


class _(str):

    observers = []
    lang = None

    def __new__(cls, s, *args, **kwargs):
        if _.lang is None:
            _.switch_lang('en_GB')
        s = _.translate(s, *args, **kwargs)
        return super(_, cls).__new__(cls, s)

    @staticmethod
    def translate(s, *args, **kwargs):
        return _.lang(s).format(args, kwargs)

    @staticmethod
    def bind(**kwargs):
        _.observers.append(kwargs['_'])

    @staticmethod
    def switch_lang(lang):
        locale_dir = join(dirname(__file__), '..', 'resources', 'il8n', 'locales')
        locales = gettext.translation('peachyprinter', locale_dir, languages=[lang])
        _.lang = locales.gettext

        for callback in _.observers:
            callback()
