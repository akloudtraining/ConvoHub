document.getElementById('fetch-comments-btn').addEventListener('click', fetchComments);
document.getElementById('post-comment-btn').addEventListener('click', postComment);
document.getElementById('reply-comment-btn').addEventListener('click', replyToComment);
document.getElementById('fetch-trends-btn').addEventListener('click', fetchTrends);

// Fetch Comments Function
function fetchComments() {
    const videoId = document.getElementById('video-id').value;
    if (!videoId) {
        alert('Please enter a valid Video ID');
        return;
    }

    fetch(`/api/v1/comments`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            action: 'fetch',
            video_id: videoId
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch comments');
        }
        return response.json();
    })
    .then(data => {
        const commentsContainer = document.getElementById('comments-container');
        commentsContainer.innerHTML = '<h4>Comments:</h4>';
        data.items.forEach(comment => {
            const commentHtml = `
                <div class="comment-box">
                    <p><strong>${comment.snippet.topLevelComment.snippet.authorDisplayName}</strong></p>
                    <p>${comment.snippet.topLevelComment.snippet.textDisplay}</p>
                </div>`;
            commentsContainer.innerHTML += commentHtml;
        });
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while fetching comments.');
    });
}

// Post Comment Function
function postComment() {
    const videoId = document.getElementById('post-video-id').value;
    const commentText = document.getElementById('comment-text').value;

    if (!videoId || !commentText) {
        alert('Please enter both Video ID and Comment Text');
        return;
    }

    fetch(`/api/v1/comments`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            action: 'post',
            video_id: videoId,
            comment: commentText
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to post comment');
        }
        return response.json();
    })
    .then(data => {
        alert('Comment posted successfully');
        document.getElementById('comment-text').value = '';  // Clear the input after submission
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while posting the comment.');
    });
}

// Reply to Comment Function
function replyToComment() {
    const commentId = document.getElementById('reply-comment-id').value;
    const replyText = document.getElementById('reply-text').value;

    if (!commentId || !replyText) {
        alert('Please enter both Comment ID and Reply Text');
        return;
    }

    fetch(`/api/v1/comments`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            action: 'reply',
            comment_id: commentId,
            comment: replyText
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to reply to comment');
        }
        return response.json();
    })
    .then(data => {
        alert('Reply posted successfully');
        document.getElementById('reply-text').value = '';  // Clear the input after submission
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while replying to the comment.');
    });
}

// Fetch YouTube Trends Function
function fetchTrends() {
    fetch(`/api/v1/trends`, {
        method: 'GET',
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch trends');
        }
        return response.json();
    })
    .then(data => {
        const trendsContainer = document.getElementById('trends-container');
        trendsContainer.innerHTML = '<h4>Trends:</h4>';
        data.trends.forEach(trend => {
            const trendHtml = `<p>${trend}</p>`;
            trendsContainer.innerHTML += trendHtml;
        });
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while fetching trends.');
    });
}