// JavaScript for Vidya Jyoti - Unified Platform

document.addEventListener('DOMContentLoaded', function() {
    // News verification elements
    const form = document.getElementById('verificationForm');
    const verifyBtn = document.getElementById('verifyBtn');
    const spinner = document.getElementById('spinner');
    const resultsDiv = document.getElementById('news-results');
    
    // Audio upload elements
    const audioForm = document.getElementById('audioForm');
    const audioBtn = document.getElementById('audioBtn');
    const audioSpinner = document.getElementById('audioSpinner');
    const uploadZone = document.getElementById('uploadZone');
    const audioFileInput = document.getElementById('audioFile');
    const audioResults = document.getElementById('audio-results');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const headline = document.getElementById('headline').value.trim();
        if (!headline) {
            showAlert('Please enter a news headline to verify.', 'warning');
            return;
        }
        
        // Show loading state
        setLoadingState(true);
        
        try {
            const response = await fetch('/verify', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ headline: headline })
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                displayResults(data.verification_result);
            } else {
                showAlert(data.error || 'Verification failed', 'danger');
            }
            
        } catch (error) {
            console.error('Error:', error);
            showAlert('Network error. Please try again.', 'danger');
        } finally {
            setLoadingState(false);
        }
    });
    
    function setLoadingState(loading) {
        if (loading) {
            verifyBtn.disabled = true;
            spinner.classList.remove('d-none');
            verifyBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Verifying...';
        } else {
            verifyBtn.disabled = false;
            spinner.classList.add('d-none');
            verifyBtn.innerHTML = 'Verify Headline';
        }
    }
    
    function displayResults(result) {
        const scoreClass = getScoreClass(result.authenticity_score);
        
        resultsDiv.innerHTML = `
            <div class="card border-0 shadow-sm">
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-4 text-center">
                            <div class="authenticity-score ${scoreClass} pulse">
                                ${result.authenticity_score}%
                            </div>
                            <h5 class="mt-2">${result.verification_status}</h5>
                        </div>
                        <div class="col-md-8">
                            <h6>Verification Details:</h6>
                            <ul class="list-unstyled">
                                <li><strong>Sources Checked:</strong> ${result.details.total_sources_checked}</li>
                                <li><strong>Matching Sources:</strong> ${result.details.matching_sources}</li>
                                <li><strong>Methods Used:</strong> ${result.details.verification_method.join(', ')}</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            
            ${result.sources_found.length > 0 ? `
            <div class="card mt-3 border-0 shadow-sm">
                <div class="card-header">
                    <h6 class="mb-0">📰 Sources Found (${result.sources_found.length})</h6>
                </div>
                <div class="card-body">
                    ${result.sources_found.map(source => `
                        <div class="source-item p-3">
                            <div class="row">
                                <div class="col-md-8">
                                    <h6><a href="${source.url}" target="_blank">${source.title}</a></h6>
                                    <small class="text-muted">Source: ${source.source}</small><br>
                                    <small class="text-muted">Published: ${source.published_at}</small>
                                </div>
                                <div class="col-md-4 text-end">
                                    <span class="badge bg-primary">Similarity: ${source.similarity_score}%</span>
                                </div>
                            </div>
                            ${source.description ? `<p class="mt-2 mb-0 text-muted">${source.description}</p>` : ''}
                        </div>
                    `).join('')}
                </div>
            </div>
            ` : ''}
            
            <div class="summary-section">
                <h5>📋 Summary Analysis</h5>
                <div class="row">
                    <div class="col-md-6">
                        <h6>🔍 What Happened:</h6>
                        <p>${result.summary.what_happened || 'Information not available'}</p>
                        
                        <h6>📅 When:</h6>
                        <p>${result.summary.when_happened || 'Date information not available'}</p>
                    </div>
                    <div class="col-md-6">
                        <h6>📍 Where:</h6>
                        <p>${result.summary.where_happened || 'Location information not available'}</p>
                        
                        <h6>❓ Why/Context:</h6>
                        <p>${result.summary.why_happened || 'Additional context not available'}</p>
                    </div>
                </div>
            </div>
        `;
        
        resultsDiv.classList.remove('d-none');
        resultsDiv.scrollIntoView({ behavior: 'smooth' });
    }
    
    function getScoreClass(score) {
        if (score >= 70) return 'score-high';
        if (score >= 40) return 'score-medium';
        return 'score-low';
    }
    
    function showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        form.parentNode.insertBefore(alertDiv, form);
        
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
    
    // ==================== AUDIO UPLOAD FUNCTIONALITY ====================
    
    // Audio file upload handling
    if (audioForm) {
        audioForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            if (!audioFileInput.files[0]) {
                showAlert('Please select an audio file to analyze.', 'warning');
                return;
            }
            
            setAudioLoadingState(true);
            
            try {
                const formData = new FormData();
                formData.append('file', audioFileInput.files[0]);
                
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    // Redirect to results page
                    window.location.href = '/audio_result';
                } else {
                    const error = await response.json();
                    showAlert(error.error || 'Audio analysis failed', 'danger');
                }
                
            } catch (error) {
                console.error('Error:', error);
                showAlert('Network error. Please try again.', 'danger');
            } finally {
                setAudioLoadingState(false);
            }
        });
    }
    
    // Audio file drag and drop
    if (uploadZone) {
        uploadZone.addEventListener('click', () => audioFileInput.click());
        
        uploadZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadZone.classList.add('dragover');
        });
        
        uploadZone.addEventListener('dragleave', () => {
            uploadZone.classList.remove('dragover');
        });
        
        uploadZone.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadZone.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleAudioFileSelect(files[0]);
            }
        });
    }
    
    if (audioFileInput) {
        audioFileInput.addEventListener('change', (e) => {
            if (e.target.files[0]) {
                handleAudioFileSelect(e.target.files[0]);
            }
        });
    }
    
    function handleAudioFileSelect(file) {
        const allowedTypes = ['audio/mp3', 'audio/mpeg', 'audio/wav', 'audio/flac', 'audio/m4a', 'audio/ogg'];
        const allowedExtensions = ['.mp3', '.wav', '.flac', '.m4a', '.ogg'];
        
        const fileName = file.name.toLowerCase();
        const isValidExtension = allowedExtensions.some(ext => fileName.endsWith(ext));
        
        if (!isValidExtension) {
            showAlert('Please select a valid audio file (MP3, WAV, FLAC, M4A, OGG)', 'warning');
            return;
        }
        
        if (file.size > 50 * 1024 * 1024) { // 50MB limit
            showAlert('File size must be less than 50MB', 'warning');
            return;
        }
        
        // Update UI to show selected file
        const uploadContent = uploadZone.querySelector('.upload-content');
        uploadContent.innerHTML = `
            <i class="fas fa-file-audio fa-3x text-success mb-3"></i>
            <h5>File Selected</h5>
            <p class="text-muted">${file.name}</p>
            <small class="text-success">Ready for analysis</small>
        `;
        
        audioBtn.disabled = false;
    }
    
    function setAudioLoadingState(loading) {
        if (loading) {
            audioBtn.disabled = true;
            audioSpinner.classList.remove('d-none');
            audioBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Analyzing...';
        } else {
            audioBtn.disabled = false;
            audioSpinner.classList.add('d-none');
            audioBtn.innerHTML = '<i class="fas fa-brain me-2"></i>Analyze Audio';
        }
    }
    
    // ==================== NAVIGATION SMOOTH SCROLLING ====================
    
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});