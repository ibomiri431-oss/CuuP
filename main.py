from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import itertools
import random
from datetime import datetime
from pathlib import Path

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

class Profile(BaseModel):
    name: str
    surname: str = ""
    nick: str = ""
    birthdate: str = ""
    wife: str = ""
    wifen: str = ""
    wifeb: str = ""
    kid: str = ""
    kidn: str = ""
    kidb: str = ""
    pet: str = ""
    company: str = ""
    words: str = ""
    spechars: bool = True
    randnum: bool = True
    leetmode: bool = True

class CuppEngine:
    def __init__(self):
        self.CONFIG = {
            "chars": ["!", "@", "#", "$", "%", "&", "*"],
            "numfrom": 0,
            "numto": 100,
            "leet": {
                'a': ['4', '@'], 'e': ['3'], 'i': ['1', '!'], 
                'o': ['0'], 's': ['$', '5'], 't': ['7'], 
                'g': ['9'], 'z': ['2']
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

    def generate_wordlist(self, profile: Profile):
        chars = self.CONFIG["chars"]
        current_year = datetime.now().year
        years = [str(y) for y in range(current_year - 5, current_year + 2)]
        
        # Helper extraction
        name = profile.name
        surname = profile.surname
        nick = profile.nick
        birthdate = profile.birthdate
        wife = profile.wife
        wifen = profile.wifen
        wifeb = profile.wifeb
        kid = profile.kid
        kidn = profile.kidn
        kidb = profile.kidb
        pet = profile.pet
        company = profile.company
        words = [w.strip() for w in profile.words.split(',') if w.strip()]

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

        # Capitalization
        def caps(s): return [s, s.title()] if s else []
        
        word_list_base = words + [w.title() for w in words]

        # Combinations Lists
        kombinaac = caps(pet) + caps(company)
        kombina = caps(name) + caps(surname) + caps(nick)
        kombinaw = caps(wife) + caps(wifen) + caps(surname)
        kombinak = caps(kid) + caps(kidn) + caps(surname)
        
        kombinaac = [x for x in kombinaac if x]
        kombina = [x for x in kombina if x]
        kombinaw = [x for x in kombinaw if x]
        kombinak = [x for x in kombinak if x]
        
        # Pattern Generators
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
        
        # 1. Base + Dates
        add_komb(base_mix, bdss)
        add_komb(base_mix, bdss, "_")
        add_komb(wife_mix, wbdss)
        add_komb(wife_mix, wbdss, "_")
        add_komb(kid_mix, kbdss)
        add_komb(kid_mix, kbdss, "_")
        
        # 2. Base + Years
        add_komb(base_mix, years)
        add_komb(base_mix, years, "_")
        add_komb(kombinaac, years)
        add_komb(kombinaac, years, "_")
        
        # 3. Simple Words + Dates
        add_komb(word_list_base, years)
        add_komb(word_list_base, years, "_")

        # 4. Random Numbers
        if profile.randnum:
            rng = range(self.CONFIG["numfrom"], self.CONFIG["numto"])
            for w in list(wordlist_set): # Snapshot small set
                for n in rng: 
                    wordlist_set.add(w + str(n))
            # Also add to base words
            for w in kombina:
                 for n in rng: wordlist_set.add(w + str(n))

        # 5. Special Chars
        if profile.spechars:
             current = list(wordlist_set)
             for w in current:
                 for c in self.CONFIG["chars"]:
                     wordlist_set.add(w + c)

        # 6. Leet
        if profile.leetmode:
            current = list(wordlist_set)
            for w in current:
                wordlist_set.add(self.make_leet(w))

        # Size Filtering
        final_list = [w for w in wordlist_set if 5 <= len(w) <= 30]
        
        # Save to Downloads
        downloads_path = str(Path.home() / "Downloads")
        filename = f"Wordlist_{name}_{random.randint(1000,9999)}.txt"
        filepath = os.path.join(downloads_path, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            for w in sorted(final_list):
                f.write(w + "\n")
                
        return {"filename": filename, "count": len(final_list), "path": filepath}

engine = CuppEngine()

@app.post("/generate")
async def generate(profile: Profile):
    return engine.generate_wordlist(profile)

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    # Listen on 0.0.0.0 to allow mobile access
    uvicorn.run(app, host="0.0.0.0", port=8000)
