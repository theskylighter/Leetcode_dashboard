const check_btn = document.querySelector('.check-btn');

let daily_btn =document.querySelector('#daily-btn');

// Daily Question fetcher API
async function dailyUpdate(){
    const URL = `https://alfa-leetcode-api.onrender.com/daily`;
    let response = await fetch(URL);
    let data = await response.json();
     daily_btn.href = data.questionLink;
    
}


// uncomment below line to run dailyUpdate function
dailyUpdate();

// no of Question fetcher API
check_btn.addEventListener('click', async () =>{
    const username = document.querySelector(".username").value;
    const checkOutput = document.querySelector('.check-output');
    const URL = `https://alfa-leetcode-api.onrender.com/${username}/solved`;
    
    // Show loading state
    checkOutput.classList.add('loading');
    
    try {
        const response = await fetch(URL);
        const data = await response.json();
        let solved = data.solvedProblem;
        
        // Update the solved count
        let para = document.querySelector('.num');
        para.innerText = `${solved} Q`;
        
        // Add data to leaderboard
        const tableBody = document.getElementById('leaderboard-body');
        
        // If this is the first real data, clear placeholder rows
        const isFirstEntry = tableBody.querySelector('th').textContent.trim() === '---';
        if (isFirstEntry) {
            tableBody.innerHTML = '';
        }

        // Check if user already exists in leaderboard
        const existingRow = Array.from(tableBody.getElementsByTagName('tr')).find(row => 
            row.querySelector('th').textContent.trim() === username
        );

        // If user exists, update their row, otherwise add new row
        const rowContent = `
            <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                ${username}
            </th>
            <td class="px-6 py-4">
                ${solved || 0}
            </td>
            <td class="px-6 py-4">
                ${data.easySolved || 0}
            </td>
            <td class="px-6 py-4">
                ${data.mediumSolved || 0}
            </td>
            <td class="px-6 py-4">
                ${data.hardSolved || 0}
            </td>
            <td class="px-6 py-4 text-right">
                <a href="https://leetcode.com/${username}" target="_blank" rel="noopener" 
                   class="font-medium text-blue-600 dark:text-blue-500 hover:underline">
                    Profile
                </a>
            </td>
        `;

        if (existingRow) {
            existingRow.innerHTML = rowContent;
        } else {
            const newRow = document.createElement('tr');
            newRow.className = "bg-white border-b dark:bg-gray-800 dark:border-gray-700 border-gray-200";
            newRow.innerHTML = rowContent;
            tableBody.appendChild(newRow);
        }

    } catch (error) {
        let para = document.querySelector('.num');
        para.innerText = 'Error occurred';
    } finally {
        // Hide loading state
        checkOutput.classList.remove('loading');
    }
})
// stars animation
function createStars() {
    const stars = document.querySelector('.stars');
    const count = 90; // Increase or decrease number of stars

    // Configurable attributes
    const minSize = 0.3;  // Minimum star size
    const maxSize = 3.5;  // Maximum star size
    const minDuration = 2; // Minimum twinkle duration in seconds
    const maxDuration = 5; // Maximum twinkle duration in seconds
    
    for (let i = 0; i < count; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        
        // Random position
        const x = Math.random() * 100;
        const y = Math.random() * 100;
        
        // Random size within range
        const size = minSize + Math.random() * (maxSize - minSize);
        
        // Random duration within range
        const duration = minDuration + Math.random() * (maxDuration - minDuration);
        
        star.style.cssText = `
            left: ${x}%,
            top: ${y}%,
            width: ${size}px,
            height: ${size}px,
            --duration: ${duration}s,
        `;
        
        stars.appendChild(star);
    }
}

// Call createStars when document is loaded
document.addEventListener('DOMContentLoaded', createStars);