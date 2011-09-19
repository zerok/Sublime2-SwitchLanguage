from __future__ import with_statement

import sublime
import sublime_plugin

from os.path import basename, splitext, join, dirname
import os
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
        commands_file = join(get_commands_folder(),
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


def get_commands_folder():
    """
    This method returns the folder to which this plugin writes its extra
    commands. First it tries to find its own installation path and writes
    the commands in there if the path is writable. If this is not the case
    the User's folder will be used instead.
    """
    root = sublime.packages_path()
    globstr = join(root, '**', basename(__file__))
    for file_ in glob.glob(globstr):
        dir_ = dirname(file_)
        if os.access(dir_, os.W_OK):
            return dir_
    return join(root, 'User')
