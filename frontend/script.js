// Initialize API Gateway client
const apiGatewayClient = apigClientFactory.newClient({ 'apiKey': CONFIG.API_KEY });

// Function to handle search form
async function handleSearch(event) {
    event.preventDefault();

    const query = document.getElementById('searchQuery').value.trim();
    const resultsDiv = document.getElementById('searchResults');
    resultsDiv.innerHTML = 'Searching...';

    try {
        const response = await apiGatewayClient.searchGet({ q: query });
        const photos = response.data.results;

        if (photos.length === 0) {
            resultsDiv.innerHTML = 'No results found.';
            return;
        }

        const resultsRow = document.createElement('div');
        resultsRow.className = 'row g-3';

        photos.forEach(photo => {
            const img = document.createElement('img');
            img.src = photo.url;
            img.alt = photo.labels.join(', ');
            img.className = 'img-fluid mb-3';
            
            const labels = document.createElement('p');
            labels.textContent = photo.labels.join(', ');

            const col = document.createElement('div');
            col.className = 'col-12 col-md-6 col-lg-3';

            const card = document.createElement('div');
            card.className = 'card h-100 p-3';
            
            const cardBody = document.createElement('div');
            cardBody.className = 'card-body p-0';
            
            cardBody.appendChild(labels);
            card.appendChild(img);
            card.appendChild(cardBody);
            col.appendChild(card);
            resultsRow.appendChild(col);
        });

        resultsDiv.innerHTML = '';
        resultsDiv.appendChild(resultsRow);
    } catch (error) {
        console.error('Failed to fetch photos:', error);
        resultsDiv.innerHTML = 'Failed to fetch photos.';
    }
}

// Function to handle upload form
async function handleUpload(event) {
    event.preventDefault();

    const fileInput = document.getElementById('imageFile');
    const labels = document.getElementById('customLabels').value.trim();
    const statusDiv = document.getElementById('uploadStatus');
    statusDiv.innerHTML = 'Uploading...';

    if (fileInput.files.length === 0) {
        statusDiv.innerHTML = 'Please select a file to upload.';
        return;
    }

    const file = fileInput.files[0];
    const objectKey = encodeURIComponent(file.name);
    
    try {
        // const response = await apiGatewayClient.uploadPut(
        //     {
        //         object: objectKey,
        //         'Content-Type': file.type || 'application/octet-stream',
        //         'x-amz-meta-customLabels': labels
        //     },
        //     file
        // );
        
        const response = await fetch(`${CONFIG.API_GATEWAY_URL}/upload?object=${objectKey}`, {
            method: 'PUT',
            headers: {
                'Content-Type': file.type || 'application/octet-stream',
                'x-amz-meta-customLabels': labels,
                'x-api-key': CONFIG.API_KEY
            },
            body: file
        });
        
        // console.log(response);
        statusDiv.innerHTML = 'Upload successful!';
    } catch (error) {
        console.error('Failed to upload photo:', error);
        statusDiv.innerHTML = 'Failed to upload photo.';
    }
}

function toggleForm(target) {
    const searchSection = document.getElementById('searchSection');
    const uploadSection = document.getElementById('uploadSection');

    const searchForm = document.getElementById('searchForm');
    const uploadForm = document.getElementById('uploadForm');
    const searchResults = document.getElementById('searchResults');
    const uploadStatus = document.getElementById('uploadStatus');
    
    if (target === 'upload') {
        searchForm.reset();
        searchResults.innerHTML = '';
        searchSection.classList.add('d-none');
        uploadSection.classList.remove('d-none');
    } else {
        uploadForm.reset();
        uploadStatus.innerHTML = '';
        uploadSection.classList.add('d-none');
        searchSection.classList.remove('d-none');
    }
}

// Attach handlers to forms
document.getElementById('searchForm').addEventListener('submit', handleSearch);
document.getElementById('uploadForm').addEventListener('submit', handleUpload);