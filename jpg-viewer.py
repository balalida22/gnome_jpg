#!/usr/bin/env python3
import os
import sys

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gio, Gtk


class JpgViewer(Gtk.Application):
    def __init__(self, start_path=None):
        super().__init__(application_id="local.gnome.JpgViewer")
        self.start_path = start_path
        self.window = None
        self.picture = Gtk.Picture()
        self.picture.set_can_shrink(True)

    def do_activate(self):
        self.window = Gtk.ApplicationWindow(application=self, title="JPG Viewer")
        self.window.set_default_size(900, 650)
        self.window.set_child(self.picture)

        header = Gtk.HeaderBar()
        open_button = Gtk.Button(label="Open")
        open_button.connect("clicked", self.open_dialog)
        header.pack_start(open_button)
        self.window.set_titlebar(header)

        self.window.present()
        if self.start_path:
            self.open_file(self.start_path)
        else:
            self.open_dialog()

    def open_file(self, path):
        if not path.lower().endswith((".jpg", ".jpeg")):
            self.alert("Please choose a JPG file.")
            return

        file = Gio.File.new_for_path(os.path.abspath(path))
        self.picture.set_file(file)
        self.window.set_title(os.path.basename(path))

    def open_dialog(self, *_):
        dialog = Gtk.FileChooserNative(
            title="Open JPG",
            transient_for=self.window,
            action=Gtk.FileChooserAction.OPEN,
            accept_label="Open",
            cancel_label="Cancel",
        )
        jpgs = Gtk.FileFilter()
        jpgs.set_name("JPEG images")
        jpgs.add_mime_type("image/jpeg")
        dialog.add_filter(jpgs)
        dialog.connect("response", self.on_dialog_response)
        dialog.show()

    def on_dialog_response(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            self.open_file(dialog.get_file().get_path())
        dialog.destroy()

    def alert(self, text):
        dialog = Gtk.AlertDialog(message=text)
        dialog.show(self.window)


if __name__ == "__main__":
    raise SystemExit(JpgViewer(sys.argv[1] if len(sys.argv) > 1 else None).run([sys.argv[0]]))
