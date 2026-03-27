const API_URL = "http://127.0.0.1:8000"; // Бэкенд адресі

document.addEventListener('DOMContentLoaded', () => {
    // 1. Подбор беті (major select бар болса)
    if (document.getElementById('major')) {
        loadMajors();
        setupInputForm();
    }
    
    // 2. Нәтижелер беті
    if (document.getElementById('resultsContainer')) {
        renderResults();
    }

    // 3. Университет парақшасы
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
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Есептелуде...';
        submitBtn.disabled = true;

        const userData = {
            ielts: parseFloat(document.getElementById('ielts').value) || 0,
            sat: parseInt(document.getElementById('sat').value) || null,
            gpa: parseFloat(document.getElementById('gpa').value) || 0,
            major: document.getElementById('major').value,
            require_full_grant: document.getElementById('grant').checked,
            country: "Any"
        };

        // Профильде көрсету үшін сақтаймыз
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

// --- НӘТИЖЕЛЕРДІ ШЫҒАРУ (PRO ДИЗАЙН) ---
function renderResults() {
    const resultsContainer = document.getElementById('resultsContainer');
    const displayMajor = document.getElementById('displayMajor');
    
    const userData = JSON.parse(localStorage.getItem('userData'));
    if (userData && userData.major && displayMajor) {
        displayMajor.textContent = userData.major;
    } else if (displayMajor) {
        displayMajor.textContent = "Барлығы";
    }

    const results = JSON.parse(localStorage.getItem('searchResults')) || [];
    
    // Егер ештеңе табылмаса
    if (results.length === 0) {
        resultsContainer.innerHTML = `
            <div class="glass-card" style="grid-column: 1/-1; text-align: center; padding: 40px;">
                <i class="fas fa-search" style="font-size: 3rem; color: #64748b; margin-bottom: 15px;"></i>
                <h3 style="color: white; margin-bottom: 10px;">Сәйкес бағдарлама табылмады</h3>
                <p style="color: #94a3b8;">Грант шартын алып тастап немесе басқа мамандық таңдап көріңіз.</p>
                <a href="/input.html" class="btn-primary" style="margin-top: 20px;">Қайта іздеу</a>
            </div>`;
        return;
    }

    let html = '';
    results.forEach((res, index) => {
        // Шансқа байланысты түс
        let chanceColor = res.chance >= 80 ? '#10b981' : (res.chance >= 60 ? '#f59e0b' : '#ef4444');
        let chanceBg = res.chance >= 80 ? 'rgba(16, 185, 129, 0.15)' : (res.chance >= 60 ? 'rgba(245, 158, 11, 0.15)' : 'rgba(239, 68, 68, 0.15)');

        html += `
            <div class="glass-card uni-card" data-aos="fade-up" data-aos-delay="${(index % 10) * 50}" style="display: flex; flex-direction: column; height: 100%;">
                
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px;">
                    <span style="font-size: 0.85rem; color: #94a3b8; display: flex; align-items: center; gap: 5px;">
                        <i class="fas fa-map-marker-alt"></i> ${res.university_city}, ${res.university_country}
                    </span>
                    ${res.has_full_grant ? '<span style="background: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.4); padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 800;"><i class="fas fa-award"></i> 100% ГРАНТ</span>' : ''}
                </div>
                
                <h3 style="font-size: 1.25rem; font-weight: 700; color: white; margin-bottom: 8px; line-height: 1.3;">
                    ${res.university_name}
                </h3>
                <p style="color: #cbd5e1; font-size: 0.95rem; margin-bottom: 25px; display: flex; align-items: center; gap: 8px;">
                    <i class="fas fa-book-open" style="color: var(--primary);"></i> ${res.program_name} (${res.degree})
                </p>
                
                <div style="margin-top: auto; padding-top: 15px; border-top: 1px solid rgba(255, 255, 255, 0.1); display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="display: block; font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; margin-bottom: 4px;">Мүмкіндік</span>
                        <div style="background: ${chanceBg}; color: ${chanceColor}; padding: 6px 12px; border-radius: 8px; font-weight: 800; font-size: 1.1rem; border: 1px solid ${chanceColor}40;">
                            ${res.chance}%
                        </div>
                    </div>
                    <a href="/university.html?id=${res.program_id}" class="btn-primary" style="padding: 10px 16px; font-size: 0.9rem; text-decoration: none; border-radius: 8px; transition: 0.3s;">
                        Толығырақ <i class="fas fa-arrow-right" style="margin-left: 5px; font-size: 0.8rem;"></i>
                    </a>
                </div>
            </div>
        `;
    });

    resultsContainer.innerHTML = html;
}

// --- ЖЕКЕ УНИВЕРСИТЕТ ПАРАҚШАСЫН ЖҮКТЕУ ---
async function loadUniversityDetails() {
    const urlParams = new URLSearchParams(window.location.search);
    const programId = urlParams.get('id'); 

    if (!programId) {
        document.getElementById('uniName').textContent = "Университет табылмады";
        return;
    }

    const results = JSON.parse(localStorage.getItem('searchResults')) || [];
    const uniData = results.find(r => r.program_id == programId);

    if (uniData) {
        document.getElementById('uniName').textContent = uniData.university_name;
        document.getElementById('uniLocation').textContent = `📍 ${uniData.university_city}, ${uniData.university_country}`;
        document.getElementById('uniDescription').textContent = uniData.university_desc || "Бұл Еуропадағы үздік оқу орындарының бірі. Жоғары сапалы білім мен халықаралық орта ұсынады.";
        document.getElementById('uniWebsite').href = uniData.university_website;
    }
}