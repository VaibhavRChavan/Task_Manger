document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Tabs
    setupTabs();
    
    // 2. Load initial data
    loadMeetings();

    // 3. Setup Form Listener
    const form = document.getElementById('addMeetingForm');
    if (form) {
        form.addEventListener('submit', handleMeetingSubmit);
    }
});

// --- Tab Functionality ---
function setupTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.dataset.tab;

            // Update Button Styles
            tabButtons.forEach(b => {
                b.classList.remove('active', 'text-indigo-600', 'dark:text-indigo-400', 'border-b-2', 'border-indigo-600');
                b.classList.add('text-gray-600', 'dark:text-gray-400');
            });
            btn.classList.add('active', 'text-indigo-600', 'dark:text-indigo-400', 'border-b-2', 'border-indigo-600');
            btn.classList.remove('text-gray-600', 'dark:text-gray-400');

            // Toggle Content
            tabContents.forEach(content => {
                content.style.display = 'none';
                content.classList.remove('active');
            });

            const targetContent = document.getElementById(`${targetTab}-content`);
            if (targetContent) {
                targetContent.style.display = 'block';
                targetContent.classList.add('active');
            }
        });
    });
}

// --- Form Submission (Unified) ---
async function handleMeetingSubmit(e) {
    e.preventDefault();

    const payload = {
        title: document.getElementById('meetingTitle').value.trim(),
        category: document.getElementById('meetingCategory').value,
        meeting_date: document.getElementById('meetingDate').value,
        meeting_time: document.getElementById('meetingTime').value,
        duration: parseInt(document.getElementById('meetingDuration').value || 60),
        meeting_link: document.getElementById('meetingLink').value.trim(),
        description: document.getElementById('meetingDescription').value.trim()
    };

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    try {
        const response = await fetch('/meetings/api/meetings/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.ok) {
            alert('Meeting scheduled successfully');
            e.target.reset(); // Reset the form
            loadMeetings();   // Refresh the list immediately
        } else {
            alert(data.error || 'Failed to create meeting');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Server error occurred');
    }
}

// --- Load Meetings (Secured) ---
function loadMeetings(filter = 'all') {
    fetch('/meetings/api/meetings/')
        .then(res => res.json())
        .then(data => {
            console.log("🔍 INSPECT THIS IN CONSOLE:", data);

            const container = document.getElementById('meetingsContainer');
            const emptyState = document.getElementById('emptyStateMeetings');
            
            let meetingsList = data.meetings || (Array.isArray(data) ? data : []);

            container.innerHTML = '';
            const now = new Date();
            let countTotal = 0, countUpcoming = 0, countPast = 0;
            let visibleCount = 0;

            meetingsList.forEach(m => {
                const dateStr = m.meeting_date || m.date || "";
                const timeStr = m.meeting_time || m.time || "";
                
                // FIX: Ensure we catch the description even if the key is slightly different
                const description = m.description || m.desc || ""; 
                
                const meetingDateTime = new Date(`${dateStr}T${timeStr}`);
                const isPast = meetingDateTime < now;
                const isUpcoming = meetingDateTime >= now;

                countTotal++;
                if (isUpcoming) countUpcoming++;
                if (isPast) countPast++;

                if (filter === 'upcoming' && !isUpcoming) return;
                if (filter === 'past' && !isPast) return;

                visibleCount++;

                const div = document.createElement('div');
                // We use flex-col so the description can sit UNDER the title/date
                div.className = 'bg-white dark:bg-gray-800 p-5 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 flex flex-col gap-3 mb-4';
                
                div.innerHTML = `
                    <div class="flex justify-between items-start">
                        <div class="flex-1">
                            <h4 class="font-bold text-lg text-gray-800 dark:text-white leading-tight">${m.title}</h4>
                            <div class="flex items-center gap-4 mt-2 text-sm text-gray-500">
                                <span>📅 ${dateStr}</span>
                                <span>⏰ ${timeStr}</span>
                            </div>
                        </div>
                        ${m.meeting_link ? `
                            <a href="${m.meeting_link}" target="_blank" class="shrink-0 bg-purple-600 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-purple-700 transition">
                                Join
                            </a>
                        ` : ''}
                    </div>

                    ${description ? `
                        <div class="mt-2 py-3 px-4 bg-gray-50 dark:bg-gray-700/50 rounded-xl">
                            <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed">
                                ${description}
                            </p>
                        </div>
                    ` : `
                        <p class="text-xs text-gray-400 italic">No description provided.</p>
                    `}
                `;
                container.appendChild(div);
            });

            // Update Cards
            if(document.getElementById('totalMeetings')) document.getElementById('totalMeetings').innerText = countTotal;
            if(document.getElementById('upcomingMeetings')) document.getElementById('upcomingMeetings').innerText = countUpcoming;
            if(document.getElementById('pastMeetings')) document.getElementById('pastMeetings').innerText = countPast;

            if (emptyState) {
                visibleCount === 0 ? emptyState.classList.remove('hidden') : emptyState.classList.add('hidden');
            }
        })
        .catch(err => console.error("Fetch error:", err));
}
document.querySelectorAll('.meeting-filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.meeting-filter-btn')
            .forEach(b => b.classList.remove('bg-purple-600', 'text-white'));

        btn.classList.add('bg-purple-600', 'text-white');

        loadMeetings(btn.dataset.filter);
    });
});
