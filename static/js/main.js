// Create animated stars background
function createStars() {
    const starsContainer = document.querySelector('.stars');
    const numberOfStars = 100;

    for (let i = 0; i < numberOfStars; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.left = Math.random() * 100 + '%';
        star.style.top = Math.random() * 100 + '%';
        star.style.animationDelay = Math.random() * 4 + 's';
        star.style.animationDuration = (Math.random() * 3 + 2) + 's';
        starsContainer.appendChild(star);
    }
}

// Tab switching functionality
function switchTab(tabName) {
    const tabs = document.querySelectorAll('.tab');
    const contents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => tab.classList.remove('active'));
    contents.forEach(content => content.classList.remove('active'));

    document.querySelector(`[onclick="switchTab('${tabName}')"]`).classList.add('active');
    document.getElementById(`${tabName}-tab`).classList.add('active');
}

// Handle file upload
function handleFileUpload(event) {
    const file = event.target.files[0];
    const label = document.querySelector('.file-upload-label p');

    if (file) {
        label.textContent = `Selected: ${file.name}`;
    }

}

function getInputCSV() {
    const file = document.getElementById('data-file').files[0];
    if (!file) {
        alert('Please upload a CSV file.');
        return;
    }
    const reader = new FileReader();

    reader.onload = function (e) {
        const text = e.target.result;
        console.log(text);
        // Parse CSV content using PapaParse
        const parsedData = Papa.parse(text, {
            header: true,
            dynamicTyping: true,
            skipEmptyLines: true
        });
        console.log('Parsed Data:', parsedData.data);
    }
    reader.readAsText(file);
}
// Simulate data analysis
function analyzeData() {
    const progressBar = document.getElementById('analysis-progress');
    const progressFill = document.getElementById('progress-fill');
    const resultsDiv = document.getElementById('prediction-results');

    resultsDiv.style.display = 'none';

    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress >= 100) {
            progress = 100;
            clearInterval(interval);
            setTimeout(showResults, 500);
        }
        progressFill.style.width = progress + '%';
    }, 200);
}

function showResults() {
    const progressBar = document.getElementById('analysis-progress');
    const resultsDiv = document.getElementById('prediction-results');
    const resultDisplay = document.getElementById('result-display');
    const classification = document.getElementById('result-classification');
    const confidence = document.getElementById('result-confidence');
    const confidenceBar = document.getElementById('confidence-bar');
    const description = document.getElementById('result-description');

    progressBar.style.display = 'none';
    resultsDiv.style.display = 'block';

    // // Simulate random results
    const outcomes = [
        {
            type: 'confirmed',
            class: '',
            title: 'Confirmed Exoplanet',
        },
        {
            type: 'candidate',
            class: 'candidate',
            title: 'Planetary Candidate',
        },
        {
            type: 'false-positive',
            class: 'false-positive',
            title: 'False Positive',
        }
    ];

    const result = outcomes[Math.floor(Math.random() * outcomes.length)];

    resultDisplay.className = 'prediction-result ' + result.class;
    classification.textContent = 'Classification: ' + result.title;
    confidence.textContent = 'Confidence: ' + result.conf + '%';
    confidenceBar.style.width = result.conf + '%';
    description.textContent = result.desc;

    // Update chart placeholder
    document.getElementById('chart-area').innerHTML = `
    <div style="text-align: center; padding: 50px;">
        <h4 style="color: #64b5f6; margin-bottom: 20px;">Transit Detection Analysis</h4>
        <p style="color: #b0b0b0;">Classification: ${result.title}</p>
        <p style="color: #b0b0b0;">Confidence Score: ${result.conf}%</p>
        <div style="margin-top: 30px; padding: 20px; background: rgba(100, 181, 246, 0.1); border-radius: 8px;">
            <p style="font-size: 0.9rem; color: #e0e0e0;">Interactive light curve visualization would be displayed here with real data processing</p>
        </div>
    </div>
    `;
}

function processUploadedData() {
    const file = document.getElementById('data-file').files[0];
    if (!file) {
        alert('Please upload a CSV file.');
        return;
    }
    const btn = document.getElementById('process-dataset-btn');
    btn.disabled = true;
    btn.textContent = 'Processing...';
    const formData = new FormData();
    formData.append('file', file);
    const model_name = document.getElementById('model-name').value;
    formData.append('model', model_name);
    console.log('form data:', formData);

    fetch('/predict/csv', {
        method: 'POST',
        body: formData
    })
        .then(response => {
            const msg = document.getElementById('error-message');
            if (!response.ok) {
                console.error('Server error:', response.status);
                msg.style.display = 'inline-block';
                if (response.status === 413) {
                    // alert('File is too large. Please upload a smaller file.');
                    msg.textContent = 'File is too large. Please upload a smaller file.';
                } else if (response.status === 422) {
                    response.json().then(data => {
                        msg.textContent = data.message || 'Invalid file format. Please ensure the CSV contains the required columns.';
                    });
                }
                else {
                    msg.textContent = 'Error uploading file. Please try again.';
                }
            } else {
                msg.style.display = 'none';
            }
            return response.text(); // instead of response.body
        })
        .then(data => {
            console.log(data);
            const resultSection = document.getElementById('csv-result-section');
            const results = document.getElementById('results');
            resultSection.innerHTML = data; // safely inject HTML/text
            results.style.display = 'block';

            // Ensure result table behaviors are bound after dynamic injection
            const ensureResultTableInit = () => {
                try {
                    if (window.initResultTable) {
                        window.initResultTable();
                    }
                } catch (e) {
                    console.error('Failed to initialize result table:', e);
                }
            };

            if (typeof window.initResultTable === 'function') {
                ensureResultTableInit();
            } else {
                const existingScript = document.querySelector('script[src="static/js/result-table.js"]');
                if (existingScript) {
                    // If script tag exists (e.g., injected), reappend to force execution
                    const script = document.createElement('script');
                    script.src = 'static/js/result-table.js';
                    script.onload = ensureResultTableInit;
                    document.body.appendChild(script);
                } else {
                    const script = document.createElement('script');
                    script.src = 'static/js/result-table.js';
                    script.onload = ensureResultTableInit;
                    document.body.appendChild(script);
                }
            }
        })
        .catch(error => {
            console.error('Error processing file:', error);
        })
        .finally(() => {
            btn.disabled = false;
            btn.textContent = 'Process Dataset';
            document.getElementById('csv-result-section').scrollIntoView({ behavior: 'smooth' });
        });

}

function trainModel() {
    const trainButton = document.getElementById('train-model-btn');
    const nameInput = document.getElementById('custom-model-name');
    const filesInput = document.getElementById('custom-data-files');

    const modelName = nameInput.value && nameInput.value.trim();
    const files = filesInput.files;

    if (!modelName) {
        alert('Please enter a model name.');
        return;
    }
    if (!files || files.length === 0) {
        alert('Please upload at least one CSV file.');
        return;
    }

    const fd = new FormData();
    fd.append('model_name', modelName);
    for (let i = 0; i < files.length; i++) {
        fd.append('files', files[i]);
    }

    trainButton.disabled = true;
    const originalText = trainButton.textContent;
    trainButton.textContent = 'Training...';

    fetch('/custom-model/train', {
        method: 'POST',
        body: fd
    })
        .then(async (res) => {
            if (!res.ok) {
                const data = await res.json().catch(() => ({}));
                throw new Error(data.message || 'Failed to train model');
            }
            return res.json();
        })
        .then((data) => {
            trainButton.textContent = 'Model Trained! Refreshing...';
            // refresh the page to fetch updated models list
            setTimeout(() => {
                window.location.reload();
            }, 800);
        })
        .catch((err) => {
            alert(err.message);
        })
        .finally(() => {
            trainButton.disabled = false;
            trainButton.textContent = originalText;
        });
}


function getPredictManual() {
    const analyzeButton = document.getElementById('analyze-data-button');
    analyzeButton.disabled = true;
    analyzeButton.textContent = 'Analyzing...';
    const form = document.getElementById('exoplanet-form');
    const formData = new FormData(form);
    const model_name = document.getElementById('model-name').value;
    const data = {
        "model": model_name
    };
    formData.forEach((value, key) => {
        data[key] = value;
    });
    console.log('Form Data:', data);

    const jsonData = JSON.stringify(data);
    fetch(`/predict/manual`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: jsonData
    }).then(response => response.json())
        .then(data => {
            console.log('Prediction result:', data);
            const resultsDiv = document.getElementById('prediction-results');
            const resultDisplay = document.getElementById('result-display');
            const classification = document.getElementById('result-classification');
            const resultClassificationMessage = document.getElementById('result-classification-message');
            resultsDiv.style.display = 'block';

            const mapper = {
                'False Positive': 'false-positive',
                'Candidate': 'candidate',
                'Confirmed': ''
            };
            resultDisplay.className = 'prediction-result ' + mapper[data.prediction];
            classification.textContent = 'Classification: ' + data.prediction;
            if (data.prediction != 'Confirmed') {
                resultClassificationMessage.innerHTML = `<sub> <a href="/learn#why-every-dip-is-not-a-exoplanet" style="color: white;">Why Not?</a>
                            </sub>`
            } else {
                resultClassificationMessage.innerHTML = ''
            }
        })
        .catch(error => {
            alert('Error getting prediction. Please ensure all fields are filled correctly.');
            console.error('Error getting prediction:', error);
        })
        .finally(() => {
            analyzeButton.disabled = false;
            analyzeButton.textContent = 'Analyze Data';
        });
}
// Initialize the interface
document.addEventListener('DOMContentLoaded', function () {
    createStars();
    try {
        const modelSelect = document.getElementById('model-name');
        const refreshCM = () => {
            const model = modelSelect && modelSelect.value;
            if (!model) return;
            fetch(`/model/${encodeURIComponent(model)}/confusion-matrix`).then(r => r.json()).then(data => {
                if (!data || !data.confusion_matrix) return;
                const cm = data.confusion_matrix; // assume 3x3 order: [Confirmed, Candidate, False Positive]
                // Map cells: rows actual (Confirmed, Candidate, False Positive), cols predicted same order
                const safe = (v) => (typeof v === 'number' ? v : 0);
                // Row 0: Confirmed → [TT, TC, TF]
                const r0 = cm[0] || [];
                document.getElementById('cm-tt') && (document.getElementById('cm-tt').textContent = safe(r0[0]));
                document.getElementById('cm-tc') && (document.getElementById('cm-tc').textContent = safe(r0[1]));
                document.getElementById('cm-tf') && (document.getElementById('cm-tf').textContent = safe(r0[2]));
                // Row 1: Candidate → [CT, CC, CF]
                const r1 = cm[1] || [];
                document.getElementById('cm-ct') && (document.getElementById('cm-ct').textContent = safe(r1[0]));
                document.getElementById('cm-cc') && (document.getElementById('cm-cc').textContent = safe(r1[1]));
                document.getElementById('cm-cf') && (document.getElementById('cm-cf').textContent = safe(r1[2]));
                // Row 2: False Positive → [FT, FC, FF]
                const r2 = cm[2] || [];
                document.getElementById('cm-ft') && (document.getElementById('cm-ft').textContent = safe(r2[0]));
                document.getElementById('cm-fc') && (document.getElementById('cm-fc').textContent = safe(r2[1]));
                document.getElementById('cm-ff') && (document.getElementById('cm-ff').textContent = safe(r2[2]));
            }).catch(() => { /* ignore */ });
        };
        modelSelect && modelSelect.addEventListener('change', refreshCM);
        refreshCM();
    } catch { }
});

try {

    // Form submission handler

    // document.getElementById('exoplanet-form').addEventListener('submit', function (e) {
    //     e.preventDefault();
    //     analyzeData();
    // });
    document.addEventListener('DOMContentLoaded', () => {

        document.getElementById('exoplanet-form').addEventListener('submit', function (e) {
            e.preventDefault(); // stop the browser’s default submit
            console.log('Manual form submitted');
            getPredictManual();
        });

    });
} catch {

}

