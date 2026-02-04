import customtkinter as ctk
import os
import itertools
import random
import threading
from datetime import datetime
from pathlib import Path

# --- CUPP Motoru (Aynı Mantık) ---

class CuppEngine:
    def __init__(self):
        self.CONFIG = {
            "chars": ["!", "@", "#", "$", "%", "&", "*"], 
            "numfrom": 0,
            "numto": 100, 
            "leet": {
                'a': ['4', '@'], 'e': ['3'], 'i': ['1', '!'], 
                'o': ['0'], 's': ['$', '5'], 't': ['7'], 
                'g': ['9'], 'z': ['2'], 'c': ['(']
            }
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

    def generate_wordlist(self, profile, update_callback=None):
        if update_callback: update_callback(0.1, "Analiz Başlatılıyor...")

        chars = self.CONFIG["chars"]
        current_year = datetime.now().year
        years = [str(y) for y in range(current_year - 5, current_year + 2)]
        
        # Profil Verilerini Al
        name = profile.get("name", "")
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

        # --- Veri İşleme ---
        
        def parse_bd(bd):
            if len(bd) == 8:
                return [bd[-2:], bd[-3:], bd[-4:], bd[1:2], bd[3:4], bd[:2], bd[2:4]]
            return []

        bdss = parse_bd(birthdate)
        wbdss = parse_bd(wifeb)
        kbdss = parse_bd(kidb)
        
        if birthdate: bdss += years
        if wifeb: wbdss += years
        if kidb: kbdss += years

        # Büyük/Küçük Harf Varyasyonları
        def caps(s): return [s, s.title()] if s else []
        
        word_list_base = words + [w.title() for w in words]

        kombinaac = caps(pet) + caps(company)
        kombina = caps(name) + caps(surname) + caps(nick)
        kombinaw = caps(wife) + caps(wifen) + caps(surname)
        kombinak = caps(kid) + caps(kidn) + caps(surname)
        
        kombinaac = [x for x in kombinaac if x]
        kombina = [x for x in kombina if x]
        kombinaw = [x for x in kombinaw if x]
        kombinak = [x for x in kombinak if x]
        
        # Kombinasyonlar
        wordlist_set = set()

        def mix_lists(list1, list2):
            res = []
            for i in list1:
                res.append(i)
                for j in list2:
                    if i != j: res.append(i+j)
            return res

        base_mix = mix_lists(kombina, kombina)
        wife_mix = mix_lists(kombinaw, kombinaw)
        kid_mix = mix_lists(kombinak, kombinak)

        def add_komb(seq, suffixes, sep=""):
            for w in seq:
                for s in suffixes:
                    wordlist_set.add(w + sep + s)
        
        if update_callback: update_callback(0.3, "Kombinasyonlar Oluşturuluyor...")
        
        # 1. Temel + Tarihler
        add_komb(base_mix, bdss)
        add_komb(base_mix, bdss, "_")
        add_komb(wife_mix, wbdss)
        add_komb(wife_mix, wbdss, "_")
        add_komb(kid_mix, kbdss)
        add_komb(kid_mix, kbdss, "_")
        
        # 2. Temel + Yıllar
        add_komb(base_mix, years)
        add_komb(base_mix, years, "_")
        add_komb(kombinaac, years)
        add_komb(kombinaac, years, "_")
        
        # 3. Ek Kelimeler + Tarihler
        add_komb(word_list_base, bdss)
        add_komb(word_list_base, bdss, "_")
        add_komb(word_list_base, kbdss)
        add_komb(word_list_base, years)

        # 4. Rastgele Sayılar
        if profile.get("randnum"):
            if update_callback: update_callback(0.5, "Rastgele Sayılar Ekleniyor...")
            rng = range(self.CONFIG["numfrom"], self.CONFIG["numto"])
            temp_set = list(wordlist_set) # Snapshot
            # Hepsine değil, sadece temel kelimelere ekleyelim ki çok şişmesin
            target_list = kombina + kombinaac + word_list_base
            for w in target_list:
                for n in rng: 
                    wordlist_set.add(w + str(n))

        # 5. Özel Karakterler
        if profile.get("spechars"):
            if update_callback: update_callback(0.7, "Özel Karakterler Entegre Ediliyor...")
            special_chars = self.CONFIG["chars"]
            current = list(wordlist_set)
            # Performans için sadece %10'una veya kısa olanlara ekleme yapmıyoruz, hepsine yapıyoruz ama basit
            for w in current:
                for c in special_chars:
                    wordlist_set.add(w + c)

        # 6. Leet Mode
        if profile.get("leetmode"):
            if update_callback: update_callback(0.8, "Hacker Dili (L33t) Uygulanıyor...")
            current = list(wordlist_set)
            for w in current:
                wordlist_set.add(self.make_leet(w))

        # Filtreleme
        final_list = [w for w in wordlist_set if 5 <= len(w) <= 30]

        if update_callback: update_callback(0.9, "Dosyaya Yazılıyor...")
        
        # İndirilenler Klasörüne Kayıt
        downloads_path = str(Path.home() / "Downloads")
        filename = f"Wordlist_{name}_{random.randint(1000,9999)}.txt"
        filepath = os.path.join(downloads_path, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            for w in sorted(final_list):
                f.write(w + "\n")

        return filepath, len(final_list)

# --- Modern GUI (Cyberpunk Style) ---

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Cyberpunk Colors
        self.col_bg = "#050510"
        self.col_panel = "#0F172A"
        self.col_accent = "#00f3ff" # Neon Cyan
        self.col_text = "#e0faff"
        self.col_btn = "#1e293b"
        self.col_btn_hover = "#334155"
        
        ctk.set_appearance_mode("dark")
        # Custom color theme is tricky without a json file, so we manually configure colors
        
        self.title("NEXUS WORDLIST GENERATOR V2")
        self.geometry("480x850")
        self.configure(fg_color=self.col_bg)
        
        # Scrollable Main Area
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Header
        self.header_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.header_frame.pack(pady=(20, 20))
        
        self.lbl_title = ctk.CTkLabel(self.header_frame, text="NEXUS", 
                                      font=ctk.CTkFont(family="Orbitron", size=32, weight="bold"),
                                      text_color=self.col_accent)
        self.lbl_title.pack()
        
        self.lbl_sub = ctk.CTkLabel(self.header_frame, text="GELİŞMİŞ PAROLA PROFİLLEYİCİ", 
                                    font=ctk.CTkFont(size=12, weight="bold"),
                                    text_color="gray")
        self.lbl_sub.pack()

        # --- Sections ---
        
        self.add_section("🎯 HEDEF BİLGİLERİ")
        self.entry_name = self.add_entry("Adı (Zorunlu)")
        self.entry_surname = self.add_entry("Soyadı")
        self.entry_nick = self.add_entry("Takma Adı")
        self.entry_bd = self.add_entry("Doğum Tarihi (GGAAAAYYYY)")

        self.add_section("❤️ EŞ / SEVGİLİ")
        self.entry_pname = self.add_entry("Eşin Adı")
        self.entry_pnick = self.add_entry("Eşin Takma Adı")
        self.entry_pbd = self.add_entry("Eşin D.Tarihi (GGAAAAYYYY)")

        self.add_section("⚡ EKSTRA DETAYLAR")
        self.entry_cname = self.add_entry("Çocuk Adı")
        self.entry_pet = self.add_entry("Evcil Hayvan")
        self.entry_company = self.add_entry("Şirket Adı")
        self.entry_keywords = self.add_entry("Ekstra Kelimeler (Virgülle)")

        # Settings
        self.add_section("⚙️ AYARLAR")
        
        self.switch_specials = self.add_switch("Özel Karakterler (!@#)")
        self.switch_numbers = self.add_switch("Rastgele Sayılar (0-100)")
        self.switch_leet = self.add_switch("Hacker Dili (L33t M0d3)")

        # Generate Button
        self.btn_gen = ctk.CTkButton(self.scroll_frame, text="HARMANLAMAYI BAŞLAT", height=50, 
                                     font=ctk.CTkFont(size=15, weight="bold"),
                                     fg_color=self.col_accent, text_color="black",
                                     hover_color="#00bcd4",
                                     corner_radius=10,
                                     command=self.start_gen)
        self.btn_gen.pack(fill="x", padx=20, pady=30)

        # Feedback
        self.progress = ctk.CTkProgressBar(self.scroll_frame, progress_color=self.col_accent)
        self.progress.set(0)
        self.progress.pack(fill="x", padx=20, pady=(0,10))
        self.progress.pack_forget()

        self.lbl_status = ctk.CTkLabel(self.scroll_frame, text="", text_color="gray")
        self.lbl_status.pack(pady=10)

    def add_section(self, text):
        f = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        f.pack(fill="x", padx=15, pady=(20, 5))
        
        l = ctk.CTkLabel(f, text=text, font=ctk.CTkFont(size=14, weight="bold"), text_color="white", anchor="w")
        l.pack(side="left")
        
        line = ctk.CTkFrame(f, height=1, fg_color="#333")
        line.pack(side="left", fill="x", expand=True, padx=(10,0))

    def add_entry(self, placeholder):
        e = ctk.CTkEntry(self.scroll_frame, placeholder_text=placeholder, height=40,
                         fg_color="#111", border_color="#333", text_color="white",
                         placeholder_text_color="gray")
        e.pack(fill="x", padx=20, pady=6)
        return e

    def add_switch(self, text):
        s = ctk.CTkSwitch(self.scroll_frame, text=text, text_color="silver", 
                          progress_color=self.col_accent, fg_color="#333")
        s.select()
        s.pack(anchor="w", padx=25, pady=8)
        return s

    def start_gen(self):
        name = self.entry_name.get()
        if not name:
            self.lbl_status.configure(text="HATA: Hedef Adı Zorunludur!", text_color="#ef4444")
            return

        self.btn_gen.configure(state="disabled", text="İŞLENİYOR...")
        self.progress.pack(fill="x", padx=20, pady=(0,10))
        
        threading.Thread(target=self.run_process, daemon=True).start()

    def run_process(self):
        profile = {
            "name": self.entry_name.get(),
            "surname": self.entry_surname.get(),
            "nick": self.entry_nick.get(),
            "birthdate": self.entry_bd.get(),
            
            "wife": self.entry_pname.get(),
            "wifen": self.entry_pnick.get(),
            "wifeb": self.entry_pbd.get(),
            
            "kid": self.entry_cname.get(),
            "kidn": "","kidb": "", # Simplified for UI cleaner look
            
            "pet": self.entry_pet.get(),
            "company": self.entry_company.get(),
            "words": [w.strip() for w in self.entry_keywords.get().split(',') if w.strip()],
            
            "spechars": self.switch_specials.get(),
            "randnum": self.switch_numbers.get(),
            "leetmode": self.switch_leet.get()
        }

        engine = CuppEngine()
        try:
            path, count = engine.generate_wordlist(profile, self.update_ui)
            self.done_ui(path, count)
        except Exception as e:
            self.update_ui(0, f"Hata: {e}")
            self.btn_gen.configure(state="normal", text="TEKRAR DENE")

    def update_ui(self, val, text):
        self.progress.set(val)
        self.lbl_status.configure(text=text)

    def done_ui(self, path, count):
        self.progress.set(1)
        self.lbl_status.configure(text=f"BAŞARILI!\nDosya: {os.path.basename(path)}\nKelime Sayısı: {count}\nKonum: İndirilenler Klasörü", text_color=self.col_accent)
        self.btn_gen.configure(state="normal", text="YENİ OLUŞTUR")
        # os.startfile(os.path.dirname(path)) # Open folder

if __name__ == "__main__":
    app = App()
    app.mainloop()
