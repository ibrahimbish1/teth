async function fetchLiveData() {
    const loading = document.getElementById('loading');
    loading.style.display = 'block'; // Show loading message
    try {
        const response = await fetch('/live-data'); // Fetch data from Flask
        if (!response.ok) {
            throw new Error('Failed to fetch live data');
        }
        const result = await response.json();
        updateTeeth(result.data); // Update teeth display
    } catch (error) {
        console.error('Error:', error);
    } finally {
        loading.style.display = 'none'; // Hide loading message
    }
}

function updateTeeth(data) {
    const container = document.getElementById('teeth-container');
    container.innerHTML = ''; // Clear existing teeth

    for (let i = 1; i <= 16; i++) {
        const tooth = document.createElement('div');
        tooth.className = 'tooth';
        tooth.textContent = `Tooth ${i}`; // Display tooth number

        const item = data.find(d => d.id === i);
        if (item) {
            // If the color is blue, make it blink between red and blue
            if (item.color === 'red') {
                tooth.classList.add('blinking'); // Add blinking effect class
            } else {
                tooth.classList.add(item.color); // Apply the regular color (red or other)
            }
        }

        container.appendChild(tooth);
    }
}

// Fetch live data every 5 seconds
setInterval(fetchLiveData, 5000);

// Initial fetch
fetchLiveData();
