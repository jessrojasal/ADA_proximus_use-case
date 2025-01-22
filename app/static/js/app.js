const API_KEY = 'b953f2d2a428582b9457ff928ae612d8a640ce87b542ff59a584c4e7b7409180' // Replace with your API key
const BASE_URL = 'http://94.110.206.175:3333/'; // Replace with your GoPhish server URL

// Fetch data from GoPhish
async function fetchData(endpoint) {
    const response = await fetch(`${BASE_URL}/${endpoint}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${API_KEY}`,
            'Content-Type': 'application/json'
        }
    });
    return response.ok ? response.json() : console.error('Failed to fetch data');
}

// Post data to GoPhish
async function postData(endpoint, data) {
    const response = await fetch(`${BASE_URL}/${endpoint}`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${API_KEY}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    return response.ok ? response.json() : console.error('Failed to post data');
}

// Example of loading campaigns
async function loadCampaigns() {
    const campaigns = await fetchData('campaigns');
    const tableBody = document.getElementById('campaigns-table');
    tableBody.innerHTML = ''; // Clear the table

    campaigns.forEach(campaign => {
        const row = `
            <tr>
                <td>${campaign.id}</td>
                <td>${campaign.name}</td>
                <td>${campaign.status}</td>
                <td>${new Date(campaign.created_date).toLocaleDateString()}</td>
                <td>
                    <button class="btn btn-sm btn-danger" onclick="deleteCampaign(${campaign.id})">Delete</button>
                </td>
            </tr>`;
        tableBody.innerHTML += row;
    });
}

// Add a new campaign
document.getElementById('add-campaign-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const campaign = {
        name: document.getElementById('campaignName').value,
        template_id: parseInt(document.getElementById('campaignTemplate').value),
        group_id: parseInt(document.getElementById('campaignGroup').value),
        page_id: parseInt(document.getElementById('campaignPage').value),
        smtp_id: parseInt(document.getElementById('campaignSMTP').value),
    };
    await postData('campaigns', campaign);
    loadCampaigns();
});

// Add a new group
document.getElementById('add-group-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const group = {
        name: document.getElementById('groupName').value,
        targets: JSON.parse(document.getElementById('groupTargets').value),
    };
    await postData('groups', group);
    alert('Group added successfully!');
});

// Initialize the dashboard
document.addEventListener('DOMContentLoaded', loadCampaigns);

