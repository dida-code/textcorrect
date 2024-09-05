# main.py
#
# Copyright 2024 Dimitrije
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from .window import TextcorrectWindow




class TextcorrectApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='io.github.dida_code.textcorrect',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('save_as', self.on_save_as_action)
        self.create_action('Open_File', self.on_open_file_action)
        self.create_action('save', self.on_save_file_action, ['<primary>s'])  # Dodajte akciju za 'save'
        self.set_accels_for_action('win.save-as', ['<Ctrl><Shift>s'])
        self.create_action('change_theme', self.on_change_theme_action)  # Dodajte akciju za promenu teme
        self.set_initial_theme()

    def set_initial_theme(self):
        """Postavlja početnu temu aplikacije."""
        # Ovdje možete koristiti GSettings ili neki drugi način da zapamtite izbor
        self.current_theme = 'dark'  # Podrazumevano na 'dark'
        self.apply_theme(self.current_theme)

    def apply_theme(self, theme):
        """Ažurira temu aplikacije."""
        sm = self.get_style_manager()
        if theme == 'dark':
            sm.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
        else:
            sm.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)

    def on_change_theme_action(self, widget, _):
        """Callback funkcija za promenu teme."""
        # Promenite temu i primenite novu
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        self.apply_theme(self.current_theme)

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = TextcorrectWindow(application=self)
            self.window = win  # Inicijalizacija atributa self.window
        win.present()

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='TextCorrect',
                                application_icon='io.github.dida_code.textcorrect',
                                developer_name='Dimitrije Kocic',
                                version='0.1.0',
                                developers=['Dimitrije Kocic'],
                                copyright='© 2024 Dimitrije Kocic')
        about.present()

    def on_save_file_action(self, widget, _):
        """Callback funkcija za čuvanje fajla."""
        if hasattr(self, 'window') and self.window:  # Proverite da li postoji prozor
            self.window.save_file_dialog(widget)  # Prosledi 'widget' kao argument
        else:
            print("Prozor nije inicijalizovan ili nije dostupan.")


    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

    def on_save_as_action(self, widget, _):
        # Pretvori self.window u Gtk.Window ako je potrebno
        parent_window = self.window if isinstance(self.window, Gtk.Window) else None

        dialog = Gtk.FileChooserDialog(
            title="Save As",
            parent=parent_window,
            action=Gtk.FileChooserAction.SAVE
        )
        dialog.add_buttons(
            "Cancel", Gtk.ResponseType.CANCEL,
            "Save", Gtk.ResponseType.ACCEPT
        )
        dialog.connect("response", self.window.on_save_response)
        dialog.show()


    def on_open_file_action(self, widget, _):
        # Pretvori self.window u Gtk.Window ako je potrebno
        parent_window = self.window if isinstance(self.window, Gtk.Window) else None

        # Kreiraj dijalog za izbor fajla
        dialog = Gtk.FileChooserDialog(
            title="Open File",
            parent=parent_window,
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            "Cancel", Gtk.ResponseType.CANCEL,
            "Open", Gtk.ResponseType.ACCEPT
        )
        dialog.connect("response", self.on_open_file_response)
        dialog.show()

    def on_open_file_response(self, dialog, response_id):
        if response_id == Gtk.ResponseType.ACCEPT:
            # Dobij fajl iz rezultata dijaloga
            file = dialog.get_file()
            if file:
                # Pročitaj sadržaj fajla
                file_content_bytes = file.load_contents(None)[1]
                file_content = None

                # Lista kodiranja koja ćemo pokušati
                encodings = ['utf-8', 'ISO-8859-1', 'Windows-1252']

                for encoding in encodings:
                    try:
                        file_content = file_content_bytes.decode(encoding)
                        print(f"Sadržaj fajla uspešno dekodiran sa {encoding} kodiranjem.")
                        break  # Ako je dekodiranje uspešno, izlazimo iz petlje
                    except UnicodeDecodeError:
                        continue  # Ako dekodiranje ne uspe, probajte sledeće

                if file_content is None:
                    print("Greška pri dekodiranju fajla sa poznatim kodiranjima.")
                    dialog.destroy()
                    return

                # Ako je dekodiranje uspelo, nastavite sa prikazom sadržaja
                print(f"Sadržaj fajla: {file_content}")
                self.window.tekst.get_buffer().set_text(file_content)

                # Sačuvajte putanju fajla u instanci ProbaWindow
                self.window.file_path = file.get_path()
        dialog.destroy()


def main(version):
    """The application's entry point."""
    app = TextcorrectApplication()
    sm = app.get_style_manager()
    sm.set_color_scheme(Adw.ColorScheme.PREFER_DARK)
    return app.run(sys.argv)

