async function startProcess() {
    const btn = document.getElementById('btnAction');
    const originalText = btn.innerText;
    
    // Loading State
    btn.innerText = 'SİSTEM İŞLENİYOR...';
    btn.disabled = true;
    btn.style.opacity = '0.7';

    const clean = (id) => {
        const el = document.getElementById(id);
        return el ? el.value : "";
    }

    const data = {
        name: clean('name'),
        surname: clean('surname'),
        nick: clean('nick'),
        birthdate: clean('birthdate'),
        
        wife: clean('wife'),
        wifen: clean('wifen'),
        wifeb: clean('wifeb'),
        
        kid: clean('kid'),
        kidn: clean('kidn'),
        kidb: clean('kidb'),
        
        pet: clean('pet'),
        company: clean('company'),
        words: clean('words'),
        
        spechars: document.getElementById('spechars').checked,
        randnum: document.getElementById('randnum').checked,
        leetmode: document.getElementById('leetmode').checked
    };

    if (!data.name) {
        alert("Hata: Hedef adı zorunludur!");
        resetBtn(btn, originalText);
        return;
    }

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        // Show Results
        document.getElementById('filePath').innerText = result.path;
        document.getElementById('resText').innerText = result.count + " adet parola kombinasyonu oluşturuldu ve Downloads klasörüne kaydedildi.";
        
        document.getElementById('resultModal').classList.remove('hidden');
        
    } catch (error) {
        console.error('Error:', error);
        alert('Sistem Hatası: Bağlantı kurulamadı.');
    } finally {
        resetBtn(btn, originalText);
    }
}

function resetBtn(btn, text) {
    btn.innerText = text;
    btn.disabled = false;
    btn.style.opacity = '1';
}

function closeModal() {
    document.getElementById('resultModal').classList.add('hidden');
    // Optional: Reset form
    // document.getElementById('nexusForm').reset(); 
}
