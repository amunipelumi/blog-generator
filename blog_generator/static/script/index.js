document.addEventListener('DOMContentLoaded', () => {
    // console.log('DOM fully loaded and parsed');
    // console.log('url: ' + endpointUrl);
    // console.log('csrf token: ' + csrftoken);
    document.getElementById('generateBlogButton').addEventListener('click', async () => {
        // console.log('Generate button clicked');
        const youtubeLink = document.getElementById('youtubeLink').value;
        const blogContent = document.getElementById('blogContent');

        if (youtubeLink) {
            // console.log('YouTube link:', youtubeLink);
            document.getElementById('loading-circle').style.display = 'block';

            blogContent.innerHTML = ''; // Clear previous content

            try {
                const response = await fetch(endpointUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken,
                    },
                    body: JSON.stringify({ link: youtubeLink }),
                });

                // console.log('Fetch response:', response);

                if (response.ok) {
                    const data = await response.json();
                    // console.log('Fetch data:', data);
                    blogContent.innerHTML = data.article;
                } else {
                    console.error('Error response:', response.statusText);
                    alert('Something went wrong. Please try again later.');
                }
            } catch (error) {
                console.error('Error occurred:', error);
                alert('Something went wrong. Please try again later.');
            }

            document.getElementById('loading-circle').style.display = 'none';
        } else {
            alert('Please enter a YouTube link.');
        }
    });
});