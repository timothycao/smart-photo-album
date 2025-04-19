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

        resultsDiv.innerHTML = '';
        photos.forEach(photo => {
            const img = document.createElement('img');
            img.src = photo.url;
            img.alt = photo.labels.join(', ');
            img.style.width = '300px';

            const labels = document.createElement('p');
            labels.textContent = photo.labels.join(', ');
            
            resultsDiv.appendChild(img);
            resultsDiv.appendChild(labels);
        });
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

// Attach handlers to forms
document.getElementById('searchForm').addEventListener('submit', handleSearch);
document.getElementById('uploadForm').addEventListener('submit', handleUpload);