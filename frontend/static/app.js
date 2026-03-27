const API_URL = "http://127.0.0.1:8000"; // Бэкенд адресі

document.addEventListener('DOMContentLoaded', () => {
    // 1. Егер подбор бетінде болсақ (major select бар)
    if (document.getElementById('major')) {
        loadMajors();
        setupInputForm();
    }
    
    // 2. Егер нәтижелер бетінде болсақ
    if (document.getElementById('resultsContainer')) {
        renderResults();
    }

    // 3. Егер жеке университет бетінде болсақ
    if (document.getElementById('universityDetails')) {
        loadUniversityDetails();
    }
});

// --- МАМАНДЫҚТАРДЫ ЖҮКТЕУ ---
async function loadMajors() {
    const majorSelect = document.getElementById('major');
    try {
        const res = await fetch(`${API_URL}/majors`);
        const majors = await res.json();
        majorSelect.innerHTML = '<option value="" disabled selected>Мамандықты таңдаңыз...</option>';
        majors.forEach(m => {
            majorSelect.innerHTML += `<option value="${m}">${m}</option>`;
        });
    } catch (e) {
        majorSelect.innerHTML = '<option value="" disabled selected>Қате шықты!</option>';
    }
}

// --- ФОРМАНЫ ЖІБЕРУ ---
function setupInputForm() {
    const inputForm = document.getElementById('inputForm');
    inputForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const submitBtn = inputForm.querySelector('button[type="submit"]');
        submitBtn.innerHTML = 'Есептелуде...';
        submitBtn.disabled = true;

        const userData = {
            ielts: parseFloat(document.getElementById('ielts').value) || 0,
            sat: parseInt(document.getElementById('sat').value) || null,
            gpa: parseFloat(document.getElementById('gpa').value) || 0,
            major: document.getElementById('major').value,
            require_full_grant: document.getElementById('grant').checked,
            country: "Any"
        };

        localStorage.setItem('userData', JSON.stringify(userData));

        try {
            const res = await fetch(`${API_URL}/calculate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(userData)
            });
            const data = await res.json();
            
            localStorage.setItem('searchResults', JSON.stringify(data.results));
            window.location.href = '/results.html'; // Нәтижелерге өту
        } catch (err) {
            alert("Қате шықты! Бэкенд қосылып тұрғанын тексеріңіз.");
            submitBtn.innerHTML = 'Нәтижені көру';
            submitBtn.disabled = false;
        }
    });
}

// --- НӘТИЖЕЛЕРДІ ШЫҒАРУ ---
function renderResults() {
    const resultsContainer = document.getElementById('resultsContainer');
    const displayMajor = document.getElementById('displayMajor');
    
    const userData = JSON.parse(localStorage.getItem('userData'));
    if (userData && userData.major && displayMajor) {
        displayMajor.textContent = userData.major;
    }

    const results = JSON.parse(localStorage.getItem('searchResults')) || [];
    
    if (results.length === 0) {
        resultsContainer.innerHTML = `<p style="grid-column: 1/-1;">Сәйкес бағдарлама табылмады. Басқа мәліметтер енгізіп көріңіз.</p>`;
        return;
    }

    let html = '';
    results.forEach(res => {
        let chanceClass = res.chance >= 80 ? 'chance-high' : (res.chance >= 60 ? 'chance-medium' : 'chance-low');

        // КАРТАДАҒЫ БАТЫРМА енді university.html-ге апарады
        html += `
            <div class="glass-card uni-card">
                <div>
                    <span style="font-size: 0.9rem; color: #ddd;">📍 ${res.university_city}, ${res.university_country}</span>
                    ${res.has_full_grant ? '<span class="grant-badge" style="float: right;">100% GRANT</span>' : ''}
                    <h3 style="margin: 10px 0;">${res.university_name}</h3>
                    <p><strong>${res.program_name}</strong> (${res.degree})</p>
                </div>
                <div style="margin-top: 20px; display: flex; justify-content: space-between; align-items: center;">
                    <div class="chance-badge ${chanceClass}">Мүмкіндік: ${res.chance}%</div>
                    <a href="/university.html?id=${res.program_id}" class="btn-primary" style="padding: 8px 12px;">Толығырақ</a>
                </div>
            </div>
        `;
    });

    resultsContainer.innerHTML = html;
}

// --- ЖЕКЕ УНИВЕРСИТЕТ ПАРАҚШАСЫН ЖҮКТЕУ ---
async function loadUniversityDetails() {
    const urlParams = new URLSearchParams(window.location.search);
    const programId = urlParams.get('id'); // Нәтижелерден келген ID

    if (!programId) {
        document.getElementById('uniName').textContent = "Университет табылмады";
        return;
    }

    // Әзірге біз нәтижелерді localStorage-тан алып, сол жерден университет ID-сін таба аламыз
    const results = JSON.parse(localStorage.getItem('searchResults')) || [];
    const uniData = results.find(r => r.program_id == programId);

    if (uniData) {
        document.getElementById('uniName').textContent = uniData.university_name;
        document.getElementById('uniLocation').textContent = `📍 ${uniData.university_city}, ${uniData.university_country}`;
        document.getElementById('uniDescription').textContent = uniData.university_desc || "Бұл Еуропадағы үздік оқу орындарының бірі. Жоғары сапалы білім мен халықаралық орта ұсынады.";
        document.getElementById('uniWebsite').href = uniData.university_website;
    }
}