document.addEventListener('DOMContentLoaded', () => {
    const kpForm = document.getElementById('kpForm');
    const chartContainer = document.getElementById('chartContainer');

    kpForm.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevent default form submission

        // Get values from input fields
        const name = document.getElementById('name').value;
        const dob = document.getElementById('dob').value;
        const pob = document.getElementById('pob').value;

        // Get time of birth values
        let hour = document.getElementById('tobHour').value;
        let minute = document.getElementById('tobMinute').value;
        const amPm = document.getElementById('tobAmPm').value;

        // Pad hour and minute with leading zero if necessary
        hour = hour.padStart(2, '0');
        minute = minute.padStart(2, '0');

        // Construct time string
        const tob = `${hour}:${minute} ${amPm}`;

        // Display pending message
        chartContainer.innerHTML = `Chart generation for ${name} with DOB ${dob}, TOB ${tob}, POB ${pob} is pending.`;
    });
});
