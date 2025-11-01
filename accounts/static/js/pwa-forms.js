// PWA Forms Integration Helper
// Use this to make forms work offline

/**
 * Enhanced form submission that handles offline mode
 * Usage: Add to form's submit event handler
 * 
 * Example:
 * form.addEventListener('submit', async (e) => {
 *     e.preventDefault();
 *     await handleFormSubmit(e.target, '/accounts/apartments/create/', 'APARTMENTS', 'create');
 * });
 */
async function handleFormSubmit(form, actionUrl, storeType, action = 'create') {
    const formData = new FormData(form);
    const data = {};
    
    // Convert FormData to object
    for (const [key, value] of formData.entries()) {
        data[key] = value;
    }

    // If offline, save to IndexedDB
    if (!navigator.onLine) {
        if (window.ApartmentDB && window.ApartmentDB.saveOffline) {
            const storeName = window.ApartmentDB.STORES[storeType];
            if (storeName) {
                try {
                    await window.ApartmentDB.saveOffline(storeName, data, action);
                    alert('Saved offline! Will sync when connection is restored.');
                    form.reset();
                    return { success: true, offline: true };
                } catch (error) {
                    console.error('Error saving offline:', error);
                    alert('Error saving offline. Please try again.');
                    return { success: false, error };
                }
            }
        }
        alert('You are offline. Data will be saved locally and synced when online.');
        return { success: false, offline: true };
    }

    // If online, submit normally
    try {
        const response = await fetch(actionUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
            },
            body: formData,
        });

        if (response.ok) {
            return { success: true, response };
        } else {
            throw new Error('Server error');
        }
    } catch (error) {
        // If network fails, save offline as fallback
        if (window.ApartmentDB && window.ApartmentDB.saveOffline) {
            const storeName = window.ApartmentDB.STORES[storeType];
            if (storeName) {
                try {
                    await window.ApartmentDB.saveOffline(storeName, data, action);
                    alert('Network error. Saved offline - will sync when connection is restored.');
                    return { success: true, offline: true };
                } catch (dbError) {
                    console.error('Error saving offline:', dbError);
                }
            }
        }
        throw error;
    }
}

// Helper to get CSRF token
function getCSRFToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find((row) => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue || '';
}

// Export for use in other scripts
window.PWAForms = {
    handleFormSubmit,
    getCSRFToken
};

