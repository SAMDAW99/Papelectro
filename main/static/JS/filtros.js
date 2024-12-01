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
