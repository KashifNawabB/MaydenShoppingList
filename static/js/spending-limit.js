function showPopup(message, type = 'success') {
    // Calculate the number of existing popups
    const existingPopups = document.querySelectorAll('.alert').length;

    // Create the new popup
    const popup = document.createElement('div');
    popup.className = `alert alert-${type} position-fixed end-0 me-4`;

    // Set the top position dynamically
    popup.style.top = `${85 + (existingPopups * 60)}px`;
    popup.style.zIndex = 1000;
    popup.textContent = message;

    // Append the popup to the body
    document.body.appendChild(popup);

    // Automatically remove the popup after 3 seconds
    setTimeout(() => {
        popup.remove();
    }, 3000);
}



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
// Function to get CSRF token from cookies
function getCSRFToken() {
    return getCookie('csrftoken');
}

$(document).ready(function() {
    const editLimitDiv = $('.edit-limit');
    const setLimitDiv = $('.set-limit');
    // Handle the edit button click
    $('#edit-spending-limit').on('click', function () {
        // Get the current spending limit
        let currentLimit = $('#current-spending-limit').text().trim();

        editLimitDiv.attr('hidden', true);

        setLimitDiv.children().find('input[type="number"]').val(currentLimit);
        setLimitDiv.attr('hidden', false);
    });

    $('#btn-set-limit').on('click', function() {
        var budget = $('#spending-limit').val()
        $.ajax({
            url: '/set-spending-limit/',
            method: 'POST',
            data: JSON.stringify({ 'budget': budget }),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': getCSRFToken() // CSRF token
            },
            success: function(response) {
                if (response.success) {
                    showPopup('Limit set successfully!', 'success');
                    setLimitDiv.attr('hidden', true);
                    editLimitDiv.children().find('#current-spending-limit').text(response.budget);
                    $('#my-budget').text(response.budget);
                    editLimitDiv.attr('hidden', false);
                } else {
                    showPopup('Failed to set limit.', 'error');
                }
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                showPopup('Failed to set limit.', 'error');
            }
        });
    })
});

