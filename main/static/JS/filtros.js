document.addEventListener('DOMContentLoaded', function () {
    const filterButton = document.querySelector('[data-bs-toggle="collapse"]');  // The filter button
    const filterContainer = document.getElementById('advancedFilter');  // The filter container

    // Function to check if the click was outside the filter container
    function closeFilterOnClickOutside(event) {
        if (!filterContainer.contains(event.target) && !filterButton.contains(event.target)) {
            // Close the collapse if clicked outside
            const collapseInstance = bootstrap.Collapse.getInstance(filterContainer);  // Get Bootstrap Collapse instance
            if (collapseInstance && collapseInstance._isShown()) {
                collapseInstance.hide();
            }
        }
    }

    // Add event listener for clicks outside the filter container
    document.addEventListener('click', closeFilterOnClickOutside);

    // Clean up the event listener on page unload
    window.addEventListener('beforeunload', function () {
        document.removeEventListener('click', closeFilterOnClickOutside);
    });
});


document.querySelectorAll('.favorito-btn').forEach((button) => {
    button.addEventListener('click', function () {
        const itemId = button.dataset.id;
        const itemType = button.dataset.type;

        const url = `/toggle-favorito/`;

        console.log('Sending request to:', url);
        console.log('ID:', itemId);
        console.log('Type:', itemType);

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken, // Ensure csrfToken is defined
            },
            body: JSON.stringify({ id: itemId, type: itemType }),
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then((data) => {
                console.log('Response:', data);
                if (data.favorito) {
                    button.innerHTML = '<i class="fas fa-star" style="color: gold;"></i>';
                } else {
                    button.innerHTML = '<i class="far fa-star"></i>';
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    });
});
