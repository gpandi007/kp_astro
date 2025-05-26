document.addEventListener('DOMContentLoaded', () => {
    const kpForm = document.getElementById('kpForm');
    const chartContainer = document.getElementById('chartContainer');

    kpForm.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevent default form submission

        // Get values from input fields
        const name = document.getElementById('name').value;
        const dob = document.getElementById('dob').value;
        const tob = document.getElementById('tob').value;
        const pob = document.getElementById('pob').value;

        // Display pending message
        chartContainer.innerHTML = `Chart generation for ${name} with DOB ${dob}, TOB ${tob}, POB ${pob} is pending.`;
    });
});
