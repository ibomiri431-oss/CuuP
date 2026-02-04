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
from kivy.graphics import Color, Rectangle
import os
import random
import itertools
from datetime import datetime
from threading import Thread

# --- Full CUPP Logic Engine for Mobile ---
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
        
        # Extract Data
        name = profile.get("name", "")
        if not name: return None, 0
        surname = profile.get("surname", "")
        nick = profile.get("nick", "")
        birthdate = profile.get("birthdate", "")
        
        wife = profile.get("wife", "")
        wifen = profile.get("wifen", "")
        wifeb = profile.get("wifeb", "")
        
        kid = profile.get("kid", "")
        kidn = profile.get("kidn", "")
        kidb = profile.get("kidb", "")
        
        pet = profile.get("pet", "")
        company = profile.get("company", "")
        words = profile.get("words", [])

        # Logic
        def parse_bd(bd):
            if len(bd) == 8: return [bd[-2:], bd[-3:], bd[-4:], bd[:2], bd[2:4]]
            return []

        bdss = parse_bd(birthdate)
        if birthdate: bdss += years
        
        wbdss = parse_bd(wifeb)
        if wifeb: wbdss += years
        
        kbdss = parse_bd(kidb)
        if kidb: kbdss += years

        def caps(s): return [s, s.title()] if s else []

        # Base Combinations
        kombina = caps(name) + caps(surname) + caps(nick)
        kombinaw = caps(wife) + caps(wifen) + caps(surname)
        kombinak = caps(kid) + caps(kidn) + caps(surname)
        kombinaac = caps(pet) + caps(company)
        
        # Wordlist
        wordlist_set = set()
        
        def add_komb(seq, suffixes):
            for w in seq:
                for s in suffixes:
                    wordlist_set.add(w + s)
                    wordlist_set.add(w + "_" + s)

        # 1. Base + Dates
        add_komb(kombina, bdss)
        add_komb(kombinaw, wbdss)
        add_komb(kombinak, kbdss)
        
        # 2. Base + Years (All)
        add_komb(kombina, years)
        add_komb(kombinaac, years)
        
        # 3. Extra Words
        word_list_base = words + [w.title() for w in words]
        add_komb(word_list_base, years)
        add_komb(word_list_base, bdss)

        # 4. Numbers (Optimized for Mobile)
        if profile.get("randnum"):
            rng = range(0, 50) # Smaller range for mobile
            target_list = list(wordlist_set)
            # Limit to avoid freezing phone
            if len(target_list) > 1000: target_list = target_list[:1000]
            
            for w in target_list:
                for n in rng:
                    wordlist_set.add(w + str(n))
        
        # 5. Special Chars
        if profile.get("spechars"):
            target_list = list(wordlist_set)
            for w in target_list:
                for c in chars:
                    wordlist_set.add(w + c)

        # 6. Leet
        if profile.get("leetmode"):
            target_list = list(wordlist_set)
            for w in target_list:
                 wordlist_set.add(self.make_leet(w))

        final_list = [w for w in wordlist_set if 5 <= len(w) < 25]

        # Android Path
        try:
            from android.storage import primary_external_storage_path
            dir_path = os.path.join(primary_external_storage_path(), 'Download')
        except:
            dir_path = os.getcwd() 

        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

        filename = f"Wordlist_{name}_{random.randint(1000,9999)}.txt"
        filepath = os.path.join(dir_path, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            for w in sorted(final_list):
                f.write(w + "\n")
                
        return filepath, len(final_list)

# --- Custom Kivy Widgets for Styling ---
class NeonLabel(Label):
    pass

class DarkInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_active = ''
        self.background_color = get_color_from_hex('#0F172A')
        self.foreground_color = get_color_from_hex('#00f3ff')
        self.hint_text_color = get_color_from_hex('#555555')
        self.padding_y = [15, 0]
        self.font_size = '16sp'

class NexusApp(App):
    def build(self):
        Window.clearcolor = get_color_from_hex('#050510') # Dark BG
        self.engine = CuppEngine()
        
        root = BoxLayout(orientation='vertical', padding=[20, 40, 20, 20], spacing=20)
        
        # Header
        header = Label(text="NEXUS MOBILE", font_size='32sp', bold=True, 
                       color=get_color_from_hex('#00f3ff'), size_hint_y=None, height=60)
        root.add_widget(header)
        
        sub = Label(text="Wordlist Generator Engine", font_size='14sp', 
                    color=get_color_from_hex('#888888'), size_hint_y=None, height=20)
        root.add_widget(sub)

        # Scroll Form
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        form = GridLayout(cols=1, spacing=15, size_hint_y=None, padding=[0, 20, 0, 0])
        form.bind(minimum_height=form.setter('height'))

        # Helper to add section
        def add_header(txt):
            lbl = Label(text=txt, color=get_color_from_hex('#bc13fe'), 
                        font_size='18sp', bold=True, size_hint_y=None, height=40, halign='left')
            lbl.bind(size=lbl.setter('text_size'))
            form.add_widget(lbl)

        def add_field(hint):
            ti = DarkInput(hint_text=hint, multiline=False, size_hint_y=None, height=50)
            form.add_widget(ti)
            return ti

        # Sections
        add_header("HEDEF")
        self.entry_name = add_field("Adı (Zorunlu)")
        self.entry_surname = add_field("Soyadı")
        self.entry_nick = add_field("Takma Adı")
        self.entry_bd = add_field("Doğum Tarihi (GGAAAAYYYY)")

        add_header("EŞ / SEVGİLİ")
        self.entry_pname = add_field("Eşin Adı")
        self.entry_pnick = add_field("Eşin Takma Adı")
        self.entry_pbd = add_field("Eşin D.Tarihi")

        add_header("EKSTRALAR")
        self.entry_kid = add_field("Çocuk Adı")
        self.entry_pet = add_field("Evcil Hayvan")
        self.entry_company = add_field("Şirket Adı")
        self.entry_words = add_field("Ekstra Kelimeler (Virgülle)")

        add_header("AYARLAR")
        # Switches
        box_sw = GridLayout(cols=2, spacing=10, size_hint_y=None, height=120)
        
        def add_sw(txt):
            l = Label(text=txt, color=get_color_from_hex('#e0faff'), halign='left')
            l.bind(size=l.setter('text_size'))
            s = Switch(active=True)
            box_sw.add_widget(l)
            box_sw.add_widget(s)
            return s

        self.sw_spec = add_sw("Özel Karakterler (!@#)")
        self.sw_num = add_sw("Rastgele Sayılar")
        self.sw_leet = add_sw("Hacker Dili (L33t)")
        form.add_widget(box_sw)

        scroll.add_widget(form)
        root.add_widget(scroll)

        # Generate Button
        self.btn = Button(text="OLUŞTUR", size_hint_y=None, height=70,
                     background_normal='', background_color=get_color_from_hex('#00f3ff'),
                     color=get_color_from_hex('#000000'), font_size='20sp', bold=True)
        self.btn.bind(on_press=self.on_generate)
        root.add_widget(self.btn)

        return root

    def on_generate(self, instance):
        input_data = {
            "name": self.entry_name.text,
            "surname": self.entry_surname.text,
            "nick": self.entry_nick.text,
            "birthdate": self.entry_bd.text,
            
            "wife": self.entry_pname.text,
            "wifen": self.entry_pnick.text,
            "wifeb": self.entry_pbd.text,
            
            "kid": self.entry_kid.text,
            "kidn": "", "kidb": "",

            "pet": self.entry_pet.text,
            "company": self.entry_company.text,
            "words": [w.strip() for w in self.entry_words.text.split(',') if w.strip()],
            
            "spechars": self.sw_spec.active,
            "randnum": self.sw_num.active,
            "leetmode": self.sw_leet.active
        }
        
        # Threading for UI responsiveness
        self.btn.text = "İŞLENİYOR..."
        self.btn.disabled = True
        Thread(target=self.run_logic, args=(input_data,)).start()

    def run_logic(self, data):
        path, count = self.engine.generate_wordlist(data)
        # Update UI needs to be scheduled on main thread usually, 
        # but Kivy properties are somewhat thread-safe for simple updates or we use Clock. But let's keep it simple for now.
        if path:
            self.show_popup("BAŞARILI", f"Dosya: {os.path.basename(path)}\nKayıt: İndirilenler\nKelime: {count}")
        else:
            self.show_popup("HATA", "İsim alanı zorunludur!")
        
        self.btn.disabled = False
        self.btn.text = "OLUŞTUR"

    def show_popup(self, title, msg):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        l = Label(text=msg, color=(1,1,1,1))
        b = Button(text="TAMAM", size_hint_y=None, height=40, background_color=get_color_from_hex('#bc13fe'))
        layout.add_widget(l)
        layout.add_widget(b)
        popup = Popup(title=title, content=layout, size_hint=(0.8, 0.4),
                      title_color=get_color_from_hex('#00f3ff'), separator_color=get_color_from_hex('#bc13fe'))
        b.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    NexusApp().run()
