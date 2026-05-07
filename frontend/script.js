// Tab switching logic
function openTab(evt, tabName) {
    const tabContents = document.getElementsByClassName("tab-content");
    for (let i = 0; i < tabContents.length; i++) {
        tabContents[i].classList.remove("active");
    }

    const tabBtns = document.getElementsByClassName("tab-btn");
    for (let i = 0; i < tabBtns.length; i++) {
        tabBtns[i].classList.remove("active");
    }

    document.getElementById(tabName).classList.add("active");
    evt.currentTarget.classList.add("active");
    
    // Hide results when switching tabs
    document.getElementById('crop-result').classList.add('hidden');
    document.getElementById('fertilizer-result').classList.add('hidden');
}

// Crop Recommendation Form Submit
document.getElementById('crop-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const btn = e.target.querySelector('button');
    const originalText = btn.innerText;
    btn.innerText = 'Analyzing...';
    btn.disabled = true;

    const data = {
        N: parseFloat(document.getElementById('crop-n').value),
        P: parseFloat(document.getElementById('crop-p').value),
        K: parseFloat(document.getElementById('crop-k').value),
        temperature: parseFloat(document.getElementById('crop-temp').value),
        humidity: parseFloat(document.getElementById('crop-hum').value),
        ph: parseFloat(document.getElementById('crop-ph').value),
        rainfall: parseFloat(document.getElementById('crop-rain').value)
    };

    try {
        const response = await fetch('/api/predict-crop', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        
        document.getElementById('crop-name').innerText = result.crop;
        // The API returns a float probability e.g., 0.85
        const confPct = (result.confidence * 100).toFixed(1);
        document.getElementById('crop-confidence').innerText = confPct;
        
        document.getElementById('crop-result').classList.remove('hidden');
    } catch (error) {
        alert('Error fetching recommendation. Is the server running?');
        console.error(error);
    } finally {
        btn.innerText = originalText;
        btn.disabled = false;
    }
});

// Fertilizer Recommendation Form Submit
document.getElementById('fertilizer-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const btn = e.target.querySelector('button');
    const originalText = btn.innerText;
    btn.innerText = 'Analyzing...';
    btn.disabled = true;

    const data = {
        temperature: parseInt(document.getElementById('fert-temp').value),
        humidity: parseInt(document.getElementById('fert-hum').value),
        moisture: parseInt(document.getElementById('fert-moist').value),
        soil_type: document.getElementById('fert-soil').value,
        crop_type: document.getElementById('fert-crop').value,
        N: parseInt(document.getElementById('fert-n').value),
        P: parseInt(document.getElementById('fert-p').value),
        K: parseInt(document.getElementById('fert-k').value)
    };

    try {
        const response = await fetch('/api/predict-fertilizer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        
        document.getElementById('fertilizer-name').innerText = result.fertilizer;
        
        document.getElementById('fertilizer-result').classList.remove('hidden');
    } catch (error) {
        alert('Error fetching recommendation. Is the server running?');
        console.error(error);
    } finally {
        btn.innerText = originalText;
        btn.disabled = false;
    }
});
