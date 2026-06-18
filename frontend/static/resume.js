const resumeFile = document.getElementById('resumeFile');
const resultBox = document.getElementById('result');
const resultTitle = document.getElementById('resultTitle');
const scoreValue = document.getElementById('scoreValue');
const skillsList = document.getElementById('skillsList');
const suggestionsList = document.getElementById('suggestionsList');

function renderResult(data) {
    resultBox.style.display = 'block';
    resultTitle.textContent = `Resume Score: ${data.score}%`;
    scoreValue.textContent = data.uploaded_at ? `Uploaded at ${data.uploaded_at}` : '';
    skillsList.innerHTML = data.skills_found && data.skills_found.length > 0
        ? data.skills_found.map(skill => `<li>${skill}</li>`).join('')
        : '<li>No skills detected. Try uploading a more complete resume.</li>';
    suggestionsList.innerHTML = data.suggestions && data.suggestions.length > 0
        ? data.suggestions.map(text => `<li>${text}</li>`).join('')
        : '<li>No suggestions available.</li>';
}

async function analyzeResume() {
    if (!resumeFile.files.length) {
        alert('Please upload a resume first');
        return;
    }

    const formData = new FormData();
    formData.append('resume', resumeFile.files[0]);

    try {
        const response = await fetch('/api/resume/analyze', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        if (!response.ok) {
            alert(result.error || 'Resume analysis failed.');
            return;
        }
        renderResult(result);
    } catch (error) {
        alert('Unable to analyze resume. Please try again.');
        console.error(error);
    }
}

async function loadLatestResume() {
    try {
        const response = await fetch('/api/resume/latest');
        if (!response.ok) return;
        const data = await response.json();
        if (data.resume) renderResult(data.resume);
    } catch (error) {
        console.warn('Could not load latest resume', error);
    }
}

loadLatestResume();