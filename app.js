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
        let para = document.querySelector('.num');
        para.innerText = `${solved} Q`;
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