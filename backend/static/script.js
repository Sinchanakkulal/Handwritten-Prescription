(() => {
  const landing = document.getElementById('landing');
  const appScreen = document.getElementById('app');
  const startBtn = document.getElementById('startBtn');
  const backBtn = document.getElementById('backBtn');

  const dropZone = document.getElementById('dropZone');
  const fileInput = document.getElementById('fileInput');
  const fileChosen = document.getElementById('fileChosen');
  const fileNameEl = document.getElementById('fileName');
  const clearFileBtn = document.getElementById('clearFileBtn');
  const uploadBtn = document.getElementById('uploadBtn');
  const uploadCard = document.getElementById('uploadCard');

  const loadingState = document.getElementById('loadingState');
  const errorState = document.getElementById('errorState');
  const resultsState = document.getElementById('resultsState');
  const extractedTextEl = document.getElementById('extractedText');
  const resultsHeading = document.getElementById('resultsHeading');
  const resultsGrid = document.getElementById('resultsGrid');
  const scanAnotherBtn = document.getElementById('scanAnotherBtn');

  let selectedFile = null;

  // ---------------- Screen switching ----------------

  startBtn.addEventListener('click', () => {
    landing.classList.add('hidden');
    appScreen.classList.remove('hidden');
  });

  backBtn.addEventListener('click', () => {
    appScreen.classList.add('hidden');
    landing.classList.remove('hidden');
    resetToUpload();
  });

  scanAnotherBtn.addEventListener('click', resetToUpload);

  function resetToUpload() {
    selectedFile = null;
    fileInput.value = '';
    fileChosen.classList.add('hidden');
    uploadBtn.disabled = true;
    uploadCard.classList.remove('hidden');
    loadingState.classList.add('hidden');
    errorState.classList.add('hidden');
    resultsState.classList.add('hidden');
  }

  // ---------------- File selection ----------------

  fileInput.addEventListener('change', (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  });

  clearFileBtn.addEventListener('click', () => {
    selectedFile = null;
    fileInput.value = '';
    fileChosen.classList.add('hidden');
    uploadBtn.disabled = true;
  });

  ['dragenter', 'dragover'].forEach((evt) => {
    dropZone.addEventListener(evt, (e) => {
      e.preventDefault();
      dropZone.classList.add('drag-over');
    });
  });

  ['dragleave', 'drop'].forEach((evt) => {
    dropZone.addEventListener(evt, (e) => {
      e.preventDefault();
      dropZone.classList.remove('drag-over');
    });
  });

  dropZone.addEventListener('drop', (e) => {
    const dropped = e.dataTransfer.files;
    if (dropped && dropped[0]) {
      setFile(dropped[0]);
    }
  });

  function setFile(file) {
    if (!file.type.startsWith('image/')) {
      showError('Please choose an image file (JPG or PNG).');
      return;
    }
    selectedFile = file;
    fileNameEl.textContent = file.name;
    fileChosen.classList.remove('hidden');
    uploadBtn.disabled = false;
  }

  // ---------------- Upload ----------------

  uploadBtn.addEventListener('click', async () => {
    if (!selectedFile) return;

    uploadCard.classList.add('hidden');
    errorState.classList.add('hidden');
    resultsState.classList.add('hidden');
    loadingState.classList.remove('hidden');

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const res = await fetch('/upload', {
        method: 'POST',
        body: formData
      });

      const data = await res.json();

      if (!res.ok || data.error) {
        throw new Error(data.error || 'Something went wrong reading that image.');
      }

      renderResults(data);
    } catch (err) {
      showError(err.message || 'Could not reach the server. Is the Flask app running?');
      uploadCard.classList.remove('hidden');
    } finally {
      loadingState.classList.add('hidden');
    }
  });

  function showError(message) {
    errorState.textContent = message;
    errorState.classList.remove('hidden');
  }

  // ---------------- Render results ----------------
  // Matches the exact shape returned by app.py's /upload route:
  // { extracted_text: str, medicines: [{ medicine_name, composition,
  //   uses, manufacturer, image_url, match_score }, ...] }

  function renderResults(data) {
    extractedTextEl.textContent = data.extracted_text || '(No text detected)';

    const medicines = Array.isArray(data.medicines) ? data.medicines : [];

    resultsHeading.textContent = medicines.length
      ? `${medicines.length} medicine${medicines.length === 1 ? '' : 's'} matched`
      : 'No medicines matched';

    resultsGrid.innerHTML = '';

    if (medicines.length === 0) {
      const p = document.createElement('p');
      p.className = 'no-results';
      p.textContent = 'Try a clearer, well-lit photo, or make sure the medicine names are legible.';
      resultsGrid.appendChild(p);
    } else {
      medicines.forEach((med) => resultsGrid.appendChild(buildMedicineCard(med)));
    }

    resultsState.classList.remove('hidden');
  }

  function buildMedicineCard(med) {
    const card = document.createElement('div');
    card.className = 'medicine-card';

    if (med.image_url && med.image_url !== 'nan') {
      const img = document.createElement('img');
      img.src = med.image_url;
      img.alt = med.medicine_name || 'Medicine';
      img.onerror = () => img.remove();
      card.appendChild(img);
    }

    const name = document.createElement('p');
    name.className = 'medicine-name';
    name.textContent = med.medicine_name || 'Unknown medicine';
    card.appendChild(name);

    card.appendChild(field('Composition', med.composition));
    card.appendChild(field('Uses', med.uses));
    card.appendChild(field('Manufacturer', med.manufacturer));

    if (typeof med.match_score === 'number') {
      const badge = document.createElement('span');
      badge.className = 'match-badge';
      badge.textContent = `${med.match_score}% match`;
      card.appendChild(badge);
    }

    return card;
  }

  function field(label, value) {
    const p = document.createElement('p');
    p.className = 'medicine-field';
    const strong = document.createElement('strong');
    strong.textContent = label + ': ';
    p.appendChild(strong);
    p.appendChild(document.createTextNode(value && value !== 'nan' ? value : '—'));
    return p;
  }
})();
