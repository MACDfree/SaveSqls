import sublime
import sublime_plugin
import os


class SavesqlCommand(sublime_plugin.TextCommand):
    def run(self, edit, filepath):
        sql = self.view.substr(sublime.Region(0, self.view.size()))
        with open(filepath,"w", encoding="utf-8") as f:
            f.write(sql)


class SqlstartCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        sublime.run_command('new_window')
        new_window = sublime.active_window()
        new_window.run_command(
            'set_layout',
            {
                "cols": [0.0, 0.33, 0.66, 1.0],
                "rows": [0.0, 1.0],
                "cells": [[0, 0, 1, 1], [1, 0, 2, 1], [2, 0, 3, 1]]
            })

        new_window.set_tabs_visible(True)
        new_window.set_sidebar_visible(False)

        new_window.focus_group(0)
        oracleview = new_window.new_file()
        oracleview.set_name("oracle")
        new_window.focus_group(1)
        sqlserverview = new_window.new_file()
        sqlserverview.set_name("sqlserver")
        new_window.focus_group(2)
        mysqlview = new_window.new_file()
        mysqlview.set_name("mysql")


class SavesqlsCommand(sublime_plugin.WindowCommand):
    """docstring for SavesqlsCommand"""
    def run(self):
        def done(filename):
            for view in views:
                dirpath = os.path.join(path, view.name())
                if os.path.exists(dirpath):
                    filepath = os.path.join(dirpath, filename + ".txt")
                    view.run_command("savesql", {"filepath": filepath})
                else:
                    filepath = os.path.join(path, filename + "_" + view.name() + ".txt")
                    view.run_command("savesql", {"filepath": filepath})

        views = self.window.views()
        settings = sublime.load_settings("SaveSqls.sublime-settings")
        path = settings.get("path")
        from datetime import datetime
        now = datetime.now()
        datestr = now.strftime("%Y%m%d")
        self.window.show_input_panel("文件名", datestr, done, None, None)

