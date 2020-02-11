import os
import datetime

import sublime
import sublime_plugin

DEFAULT_FILENAME = os.path.join("~", "notes.txt")


class Listener(sublime_plugin.ViewEventListener):
    @classmethod
    def is_applicable(cls, settings):
        return settings.has("INSERT_THE_DATE")

    @classmethod
    def applies_to_primary_view(cls):
        return True

    def on_activated(self):
        sel = self.view.sel()
        sel.clear()
        sel.add(sublime.Region(self.view.size()))

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.view.run_command("insert", args=dict(characters="\n{}\n".format(now)))

        self.view.show(self.view.size())

        self.view.settings().erase("INSERT_THE_DATE")



class OpenMyNotesAndAppendTimeCommand(sublime_plugin.WindowCommand):
    def run(self):
        settings = sublime.load_settings("MyNotes.sublime-settings")

        filename = os.path.expanduser(settings.get("path", DEFAULT_FILENAME))

        view = self.window.find_open_file(filename)

        if view:
            self.window.focus_view(view)
            view.sel().clear()
            view.sel().add(sublime.Region(view.size(), view.size()))
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            view.run_command("insert", args=dict(characters="\n{}\n".format(now)))
            self.view.show(self.view.size())
        else:
            view = self.window.open_file(filename)
            view.settings().set("INSERT_THE_DATE", True)
