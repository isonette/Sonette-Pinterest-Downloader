async function fetchVideo() {
    const urlInput = document.getElementById('urlInput');
    const resultContainer = document.getElementById('resultContainer');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const url = urlInput.value.trim();

    if (!url) return;

    // Show loading
    loadingOverlay.style.display = 'flex';

    try {
        const response = await fetch('/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();

        if (response.ok) {
            displayResult(data);
        } else {
            alert('Error: ' + (data.error || 'Failed to fetch video'));
        }
    } catch (err) {
        console.error(err);
        alert('An unexpected error occurred.');
    } finally {
        loadingOverlay.style.display = 'none';
    }
}

function displayResult(data) {
    const container = document.getElementById('resultContainer');
    // Clear previous results or placeholder
    container.innerHTML = '';

    const card = document.createElement('div');
    card.className = 'pin-card';

    // We can allow the user to play the video right there or just show thumbnail
    // Pinterest usually auto-plays.
    // Let's use the thumbnail for the "card" feel, and the download button to actually get it.
    // Or simpler: Just a video tag.

    // Check if we have a direct video url to embed

    const mediaHtml = `
        <div class="pin-media">
            <video src="${data.video_url}" poster="${data.thumbnail}" controls style="width:100%; display:block; border-radius: 16px;"></video>
            <div class="pin-overlay" style="justify-content: center; align-items: center;">
                 <!-- Overlay content if needed, maybe 'Save' button here? 
                      But native video controls might block clicks.
                      Let's put the Save button NOT in overlay for better UX on mobile/simplicity -->
            </div>
        </div>
        <div class="pin-info">
            <div class="pin-title">${data.title}</div>
            <a href="${data.video_url}" download="pinterest_video.mp4" target="_blank" class="save-btn" style="width:100%; text-align:center; margin-top:10px;">Download</a>
        </div>
    `;

    card.innerHTML = mediaHtml;
    container.appendChild(card);
}

function shareApp() {
    if (navigator.share) {
        navigator.share({
            title: 'Pinterest Downloader',
            text: 'Check out this cool video downloader!',
            url: window.location.href,
        })
            .then(() => console.log('Successful share'))
            .catch((error) => console.log('Error sharing', error));
    } else {
        // Fallback for desktop or unsupported browsers
        navigator.clipboard.writeText(window.location.href).then(function () {
            alert('Link copied to clipboard! Send it to your friends.');
        }, function (err) {
            console.error('Could not copy text: ', err);
            prompt("Copy this link to share:", window.location.href);
        });
    }
}
