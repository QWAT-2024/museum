let currentSessionId;

        // Fetch sessions
        // Fetch sessions
async function fetchSessions() {
    const res = await fetch('/get_sessions');
    const data = await res.json();
    const sessionList = document.getElementById('session-list');
    sessionList.innerHTML = '';
    data.sessions.forEach(session => {
        const li = document.createElement('li');
        li.classList.add('session-item');

        const sessionName = document.createElement('span');
        sessionName.textContent = session.name;
        sessionName.addEventListener('click', () => loadSession(session.id));
        li.appendChild(sessionName);

        const deleteButton = document.createElement('button');
        deleteButton.textContent = '❌';
        deleteButton.classList.add('delete-button');
        deleteButton.addEventListener('click', (e) => {
            e.stopPropagation(); // Prevent triggering session load
            deleteSession(session.id);
        });
        li.appendChild(deleteButton);

        sessionList.appendChild(li);
    });
}

        // Create a new session
        document.getElementById('new-session').addEventListener('click', async () => {
            const sessionName = prompt("Enter a name for the new chat session:", "New Chat");
            if (!sessionName) return;
            const res = await fetch('/new_session', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_name: sessionName })
            });
            if (res.ok) {
                const session = await res.json();
                fetchSessions();
                loadSession(session.session_id);
            } else {
                console.error("Failed to create a new session.");
            }
        });

        // Load session
        // Function to format text with *** as a new paragraph and ** as bold
        function formatResponseText(text) {
        // Replace **text** with <b>text</b>
        text = text.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');
        // Replace * with a new paragraph
        text = text.replace(/\* /g, '<br><br>');
        return text;
        }

// Delete session
async function deleteSession(sessionId) {
    if (!confirm('Are you sure you want to delete this session? This action cannot be undone.')) return;
    try {
        const res = await fetch(`/delete_session/${sessionId}`, { method: 'DELETE' });
        if (res.ok) {
            alert('Session deleted successfully.');
            fetchSessions(); // Refresh the session list
        } else {
            alert('Failed to delete the session.');
        }
    } catch (error) {
        console.error('Error deleting session:', error);
    }
}


// Load session and format messages
async function loadSession(sessionId) {
    currentSessionId = sessionId;
    const res = await fetch(`/get_history/${sessionId}`);
    const data = await res.json();
    const chatHistory = document.getElementById('chat-history');
    chatHistory.innerHTML = '';
    data.chat_history.forEach(msg => {
        const div = document.createElement('div');
        div.className = `chat-message ${msg.sender}`;
        div.innerHTML = formatResponseText(msg.message); // Apply formatting
        chatHistory.appendChild(div);
    });
}



        // Handle form submission
        document.getElementById('chat-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const queryInput = document.getElementById('query');
    const sendButton = document.querySelector('#chat-form button');
    const processing = document.getElementById('processing');

    // Disable input field and send button
    queryInput.disabled = true;
    sendButton.disabled = true;

    // Show processing text
    processing.style.display = 'block';

    const query = queryInput.value.trim();
    if (!query || !currentSessionId) {
        alert('Please create or select a session first.');
        // Re-enable input field and send button
        queryInput.disabled = false;
        sendButton.disabled = false;
        processing.style.display = 'none';
        return;
    }

    // Send the message to the backend
    try {
        const res = await fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query, session_id: currentSessionId }),
        });

        if (res.ok) {
            queryInput.value = ''; // Clear input field
            loadSession(currentSessionId); // Refresh chat history
        }
    } catch (error) {
        console.error('Error sending message:', error);
    }

    // Re-enable input field and send button
    queryInput.disabled = false;
    sendButton.disabled = false;
    processing.style.display = 'none';
});


        // Send message on pressing "Enter"
        document.getElementById('query').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                document.getElementById('chat-form').dispatchEvent(new Event('submit'));
            }
        });

        // Initial load
        fetchSessions();