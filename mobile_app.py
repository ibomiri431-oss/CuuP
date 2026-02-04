from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.switch import Switch
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
import os
import random
import itertools
from datetime import datetime
from pathlib import Path

# --- Logic Class (Embedded) ---
class CuppEngine:
    def __init__(self):
        self.CONFIG = {
            "chars": ["!", "@", "#", "$", "%", "&", "*"], 
            "numfrom": 0, "numto": 100, 
            "leet": {'a': ['4', '@'], 'e': ['3'], 'i': ['1', '!'], 'o': ['0'], 's': ['$', '5'], 't': ['7']}
        }

    def make_leet(self, x):
        res = ""
        for char in x:
            lower_char = char.lower()
            if lower_char in self.CONFIG["leet"]:
                res += random.choice(self.CONFIG["leet"][lower_char])
            else:
                res += char
        return res

    def generate_wordlist(self, profile):
        chars = self.CONFIG["chars"]
        current_year = datetime.now().year
        years = [str(y) for y in range(current_year - 5, current_year + 2)]
        
        name = profile.get("name", "")
        if not name: return None, 0

        surname = profile.get("surname", "")
        nick = profile.get("nick", "")
        birthdate = profile.get("birthdate", "")
        wife = profile.get("wife", "")
        wifen = profile.get("wifen", "")
        wifeb = profile.get("wifeb", "")
        kid = profile.get("kid", "")
        pet = profile.get("pet", "")
        company = profile.get("company", "")
        words = profile.get("words", [])

        # Logic helpers
        def parse_bd(bd):
            if len(bd) == 8: return [bd[-2:], bd[-3:], bd[-4:], bd[:2], bd[2:4]]
            return []
        
        bdss = parse_bd(birthdate) + years
        wbdss = parse_bd(wifeb) + years
        
        def caps(s): return [s, s.title()] if s else []
        
        word_list_base = words + [w.title() for w in words]
        kombina = caps(name) + caps(surname) + caps(nick)
        kombinaw = caps(wife) + caps(wifen) + caps(surname)
        
        wordlist_set = set()
        
        def add_komb(seq, suffixes):
            for w in seq:
                for s in suffixes:
                    wordlist_set.add(w + s)
                    wordlist_set.add(w + "_" + s)

        add_komb(kombina, bdss)
        add_komb(kombinaw, wbdss)
        add_komb(word_list_base, years)
        
        # Ranges
        if profile.get("randnum"):
            rng = range(0, 50) # Smaller range for mobile perf
            target = list(wordlist_set)
            for w in target[:200]: # Limit processing
                 for n in rng: wordlist_set.add(w + str(n))
        
        if profile.get("spechars"):
            target = list(wordlist_set)
            for w in target:
                for c in chars: wordlist_set.add(w + c)

        if profile.get("leetmode"):
            target = list(wordlist_set)
            for w in target: wordlist_set.add(self.make_leet(w))

        final_list = [w for w in wordlist_set if 4 <= len(w) <= 30]
        
        # Android Path Handling
        try:
            from android.storage import primary_external_storage_path
            dir_path = os.path.join(primary_external_storage_path(), 'Download')
        except:
            dir_path = os.getcwd() # Fallback for desktop testing
            
        filename = f"Wordlist_{name}_{random.randint(1000,9999)}.txt"
        filepath = os.path.join(dir_path, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            for w in sorted(final_list):
                f.write(w + "\n")
                
        return filepath, len(final_list)


# --- Kivy App ---
class NexusApp(App):
    def build(self):
        Window.clearcolor = get_color_from_hex('#050510')
        self.engine = CuppEngine()
        
        root = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Header
        root.add_widget(Label(text="[b]NEXUS MOBILE[/b]", markup=True, font_size='24sp', 
                              color=get_color_from_hex('#00f3ff'), size_hint_y=None, height=50))
        
        # Scroll View for Inputs
        scroll = ScrollView(size_hint=(1, 1))
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        def add_input(ph):
            ti = TextInput(hint_text=ph, multiline=False, size_hint_y=None, height=50,
                           background_color=get_color_from_hex('#111111'),
                           foreground_color=get_color_from_hex('#ffffff'),
                           hint_text_color=get_color_from_hex('#777777'))
            layout.add_widget(ti)
            return ti

        self.in_name = add_input("Hedef Adi (Zorunlu)")
        self.in_surname = add_input("Soyadi")
        self.in_nick = add_input("Takma Adi")
        self.in_bd = add_input("Dogum Tarihi (GGAAAAYYYY)")
        
        layout.add_widget(Label(text="Es / Sevgili Bilgileri", color=get_color_from_hex('#00f3ff'), size_hint_y=None, height=30))
        self.in_pname = add_input("Esin Adi")
        self.in_pbd = add_input("Esin D.Tarihi")
        
        layout.add_widget(Label(text="Ayarlar", color=get_color_from_hex('#00f3ff'), size_hint_y=None, height=30))
        
        # Switches
        self.sw_spec = Switch(active=True)
        layout.add_widget(Label(text="Ozel Karakterler", size_hint_y=None, height=30))
        layout.add_widget(self.sw_spec)
        
        scroll.add_widget(layout)
        root.add_widget(scroll)
        
        # Button
        btn = Button(text="OLUSTUR", size_hint_y=None, height=60,
                     background_normal='', background_color=get_color_from_hex('#00f3ff'),
                     color=get_color_from_hex('#000000'), font_size='18sp', bold=True)
        btn.bind(on_press=self.generate)
        root.add_widget(btn)
        
        return root

    def generate(self, instance):
        profile = {
            "name": self.in_name.text,
            "surname": self.in_surname.text,
            "nick": self.in_nick.text,
            "birthdate": self.in_bd.text,
            "wife": self.in_pname.text,
            "wifeb": self.in_pbd.text,
            "spechars": self.sw_spec.active,
            "randnum": True, "leetmode": True, "words": []
        }
        
        path, count = self.engine.generate_wordlist(profile)
        
        if path:
            msg = f"Basarili!\nDosya: {os.path.basename(path)}\nSayi: {count}"
        else:
            msg = "Hata: Isim gereklidir."
            
        popup = Popup(title='Durum', content=Label(text=msg), size_hint=(0.8, 0.4))
        popup.open()

if __name__ == '__main__':
    NexusApp().run()
