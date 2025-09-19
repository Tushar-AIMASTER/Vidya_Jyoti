// JavaScript for News Headline Verifier

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('verificationForm');
    const verifyBtn = document.getElementById('verifyBtn');
    const spinner = document.getElementById('spinner');
    const resultsDiv = document.getElementById('results');
    
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
});