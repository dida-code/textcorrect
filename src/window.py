# window.py
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

from gi.repository import Adw
from gi.repository import Gtk, Gdk, Gio, GLib, Pango, GdkPixbuf


@Gtk.Template(resource_path='/io/github/dida_code/textcorrect/window.ui')
class TextcorrectWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'TextcorrectWindow'

    tekst = Gtk.Template.Child()
    button = Gtk.Template.Child()
    cirilica = Gtk.Template.Child()
    latinica = Gtk.Template.Child()
    #podesavanje = Gtk.Template.Child()
    #file = Gtk.Template.Child()
    snimi = Gtk.Template.Child()
    savelabel = Gtk.Template.Child()



    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title("TextCorrect")

        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource("/io/github/dida_code/textcorrect/style.css")
        Gtk.StyleContext.add_provider_for_display(
        Gdk.Display.get_default(),
        css_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.tekst.get_style_context().add_class('tekst')




        self.button.connect("clicked", self.printText)
        self.latinica.connect("clicked", self.printLatinica)
        self.cirilica.connect("clicked", self.printCirilica)
        #self.podesavanje.connect("activate", self.prikazi_podesavanje)
        #self.file.connect("activate", self.file_choser)
        self.snimi.connect("clicked", self.save_file_dialog)

        open_action = Gio.SimpleAction(name="open")
        open_action.connect("activate", self.save_file_dialog)
        self.add_action(open_action)

        save_action = Gio.SimpleAction(name="save-as")
        save_action.connect("activate", self.save_file_dialog)
        self.add_action(save_action)

        buffer = self.tekst.get_buffer()


        self.file_path = None

        drop_target = Gtk.DropTarget.new(Gdk.FileList, Gdk.DragAction.COPY)
        drop_target.connect("drop", self.on_file_drop)

        # Povežite DropTarget sa TextView
        self.tekst.add_controller(drop_target)



    def on_file_drop(self, drop_target, value, x, y):
            file_path = value.get_files()[0].get_path()
            self.file_path = file_path
            file = Gio.File.new_for_path(file_path)
            self.load_file(file)

    def load_file(self, file):
        # Učitavanje sadržaja fajla
        file.load_contents_async(None, self.on_file_load_complete)

    def on_file_load_complete(self, file, result):
        try:
            success, contents, etag = file.load_contents_finish(result)
            if success:
                # Pokušaj dekodiranja sadržaja sa više kodiranja
                file_content = None
                encodings = ['utf-8', 'ISO-8859-1', 'Windows-1252']

                for encoding in encodings:
                    try:
                        file_content = contents.decode(encoding)
                        print(f"Sadržaj fajla uspešno dekodiran sa {encoding} kodiranjem.")
                        break  # Ako je dekodiranje uspešno, izlazimo iz petlje
                    except UnicodeDecodeError:
                        continue  # Ako dekodiranje ne uspe, probajte sledeće

                if file_content is None:
                    print("Greška pri dekodiranju fajla sa poznatim kodiranjima.")
                    return

                # Ako je dekodiranje uspelo, nastavite sa prikazom sadržaja
                buffer = self.tekst.get_buffer()
                buffer.set_text(file_content)
        except Exception as e:
            print(f"Error loading file: {e}")



    def printText(self, widget):



        replacements = {"æ":"ć","Æ":"Ć","":"ž","":"Ž","":"š","":"Š","è":"č","È":"Č","ð":"đ"}

        buffer = self.tekst.get_buffer()
        start_iter, end_iter = buffer.get_bounds()
        text = buffer.get_text(start_iter, end_iter, include_hidden_chars=True)

        for original, replacement in replacements.items():
            text = text.replace(original, replacement)

        buffer.set_text(text)

    def printCirilica(self, widget):
        replacements = {"Dj":"Ђ","dj":"ђ","Lj":"Љ","lj":"љ","Nj":"Њ","nj":"њ","Dž":"Џ","dž":"џ","B":"Б","b":"б","V":"В","v":"в","G":"Г","g":"г","D":"Д","d":"д","t":"т","Đ":"Ђ","đ":"ђ","Ž":"Ж","ž":"ж","Z":"З","z":"з","I":"И","i":"и","L":"Л","l":"л","N":"Н","n":"н","P":"П","p":"п","R":"Р","r":"р","S":"С","s":"с","Ć":"Ћ","ć":"ћ","U":"У","u":"у","F":"Ф","f":"ф","H":"Х","h":"х","C":"Ц","c":"ц","Č":"Ч","č":"ч","Š":"Ш","š":"ш"}

        buffer = self.tekst.get_buffer()
        start_iter, end_iter = buffer.get_bounds()
        text = buffer.get_text(start_iter, end_iter, include_hidden_chars=True)

        for original, replacement in replacements.items():
            text = text.replace(original, replacement)

        buffer.set_text(text)

    def printLatinica(self, widget):
        replacements = {"Љ":"Lj","љ":"lj","Њ":"Nj","њ":"nj","Џ":"Dž","џ":"dž","Б":"B","б":"b","В":"V","в":"v","Г":"G","г":"g","Д":"D","д":"d","т":"t","Ђ":"Đ","ђ":"đ","Ж":"Ž","ж":"ž","З":"Z","з":"z","И":"I","и":"i","Л":"L","л":"l","Н":"N","н":"n","П":"P","п":"p","Р":"R","р":"r","С":"S","с":"s","Ћ":"Ć","ћ":"ć","У":"U","у":"u","Ф":"F","ф":"f","Х":"H","х":"h","Ц":"C","ц":"c","Ч":"Č","ч":"č","Ш":"Š","ш":"š"}

        buffer = self.tekst.get_buffer()
        start_iter, end_iter = buffer.get_bounds()
        text = buffer.get_text(start_iter, end_iter, include_hidden_chars=True)

        for original, replacement in replacements.items():
            text = text.replace(original, replacement)

        buffer.set_text(text)
        print("jel radi")

    def save_file_dialog(self, widget):
        print(self.file_path)
        # Ako postoji file_path, snimi direktno
        if self.file_path:
            file = Gio.File.new_for_path(self.file_path)
            self.save_file(file)
        else:
            # Ako ne postoji file_path, otvori dijalog za snimanje
            dialog = Gtk.FileChooserDialog(
                title="Save As",
                parent=self,
                action=Gtk.FileChooserAction.SAVE
            )
            dialog.add_buttons(
                "Cancel", Gtk.ResponseType.CANCEL,
                "Save", Gtk.ResponseType.ACCEPT
            )
            dialog.connect("response", self.on_save_response)
            dialog.show()


    def on_save_response(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            file = dialog.get_file()
            if file:
                self.file_path = file.get_path()
                self.save_file(file)
                self.savelabel.set_text(f"File saved at: {self.file_path}")
                print(f"File saved at: {self.file_path}")

        dialog.destroy()

    def save_file(self, file):
        buffer = self.tekst.get_buffer()

        # Retrieve the iterator at the start of the buffer
        start = buffer.get_start_iter()
        # Retrieve the iterator at the end of the buffer
        end = buffer.get_end_iter()
        # Retrieve all the visible text between the two bounds
        text = buffer.get_text(start, end, False)

        # If there is nothing to save, return early
        if not text:
            return

        bytes = GLib.Bytes.new(text.encode('utf-8'))

        # Start the asynchronous operation to save the data into the file
        file.replace_contents_bytes_async(bytes,
                                          None,
                                          False,
                                          Gio.FileCreateFlags.NONE,
                                          None,
                                          self.save_file_complete)
        self.savelabel.set_text(f"File saved: {self.file_path}")
        print(f"File saved: {self.file_path}")
        GLib.timeout_add(3000, self.clear_save_message)

    def clear_save_message(self):
        # Briše tekst sa labela
        self.savelabel.set_text("")
        # Povratna vrednost False znači da se timeout ne ponavlja
        return False

    def save_file_complete(self, file, result):
        res = file.replace_contents_finish(result)
        info = file.query_info("standard::display-name",
                               Gio.FileQueryInfoFlags.NONE)
        if info:
            display_name = info.get_attribute_string("standard::display-name")
        else:
            display_name = file.get_basename()
        if not res:
            print(f"Unable to save {display_name}")


