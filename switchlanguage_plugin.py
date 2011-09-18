from __future__ import with_statement

import sublime
import sublime_plugin

from os.path import basename, splitext, dirname, abspath, join
import glob
import json


class UpdateLanguageCommands(sublime_plugin.ApplicationCommand):
    """
    Command for updating SwitchLanguage.sublime-commands file with references
    to all found .dic files.
    """
    def run(self, *args, **kwargs):
        root = sublime.packages_path()
        languages = {}
        commands_file = join(dirname(abspath(__file__)),
                'SwitchLanguage.sublime-commands')
        commands = []
        for file_ in glob.glob(u'{0}/**/*.dic'.format(root.rstrip('/'))):
            name = splitext(basename(file_))[0]
            languages[name] = join('Packages', file_[len(root):].lstrip('/'))
        for lang_name, lang_file in languages.iteritems():
            commands.append({
                'caption': u'Switch language: {0}'.format(lang_name),
                'command': 'switch_language',
                'args': {'lang': lang_file}
                })
        with open(commands_file, 'w+') as fp:
            json.dump(commands, fp, indent=4)


class SwitchLanguage(sublime_plugin.TextCommand):
    """
    Switches the current session dictionary to the given language.
    """
    def run(self, edit, lang=None):
        if lang is not None:
            self.view.settings().set('dictionary', lang)
