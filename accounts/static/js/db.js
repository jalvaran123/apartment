// Enhanced IndexedDB for Apartment PWA
// Supports: Apartments, Units, Tenants, Payments, Bills, Other Charges

const DB_NAME = "apartmentDB_v4";
const DB_VERSION = 4;

// Object stores
const STORES = {
    APARTMENTS: 'pendingApartments',
    UNITS: 'pendingUnits',
    TENANTS: 'pendingTenants',
    PAYMENTS: 'pendingPayments',
    BILLS: 'pendingBills',
    OTHER_CHARGES: 'pendingOtherCharges'
};

// Open and initialize database
function openDatabase() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open(DB_NAME, DB_VERSION);

        request.onerror = () => reject(request.error);
        request.onsuccess = () => resolve(request.result);

        request.onupgradeneeded = (event) => {
            const db = event.target.result;

            // Create object stores if they don't exist
            Object.values(STORES).forEach((storeName) => {
                if (!db.objectStoreNames.contains(storeName)) {
                    const store = db.createObjectStore(storeName, {
                        keyPath: 'tempId',
                        autoIncrement: true
                    });
                    store.createIndex('timestamp', 'timestamp', { unique: false });
                    store.createIndex('action', 'action', { unique: false });
                    console.log(`✅ Created store: ${storeName}`);
                }
            });
        };
    });
}

// Save offline data
async function saveOffline(storeName, data, action = 'create') {
    try {
        const db = await openDatabase();
        const tx = db.transaction([storeName], 'readwrite');
        const store = tx.objectStore(storeName);
        
        const record = {
            ...data,
            action, // 'create', 'update', 'delete'
            timestamp: Date.now(),
            synced: false
        };

        await store.add(record);
        console.log(`💾 Saved offline [${storeName}]:`, record);
        updateOfflineIndicator();
        return record;
    } catch (error) {
        console.error(`❌ Error saving to ${storeName}:`, error);
        throw error;
    }
}

// Get all pending data from a store
async function getPending(storeName) {
    try {
        const db = await openDatabase();
        const tx = db.transaction([storeName], 'readonly');
        const store = tx.objectStore(storeName);
        const index = store.index('synced');
        
        return new Promise((resolve, reject) => {
            const request = index.getAll(false); // Get all unsynced
            request.onsuccess = () => resolve(request.result || []);
            request.onerror = () => reject(request.error);
        });
    } catch (error) {
        console.error(`❌ Error reading from ${storeName}:`, error);
        return [];
    }
}

// Get all pending data from all stores
async function getAllPending() {
    const allPending = {};
    for (const [key, storeName] of Object.entries(STORES)) {
        allPending[key] = await getPending(storeName);
    }
    return allPending;
}

// Mark record as synced
async function markSynced(storeName, tempId) {
    try {
        const db = await openDatabase();
        const tx = db.transaction([storeName], 'readwrite');
        const store = tx.objectStore(storeName);
        
        const record = await store.get(tempId);
        if (record) {
            record.synced = true;
            await store.put(record);
        }
    } catch (error) {
        console.error(`❌ Error marking as synced:`, error);
    }
}

// Delete synced records
async function deleteSynced(storeName) {
    try {
        const db = await openDatabase();
        const tx = db.transaction([storeName], 'readwrite');
        const store = tx.objectStore(storeName);
        const index = store.index('synced');
        
        const request = index.openCursor(true); // Get all synced
        request.onsuccess = (event) => {
            const cursor = event.target.result;
            if (cursor) {
                cursor.delete();
                cursor.continue();
            }
        };
    } catch (error) {
        console.error(`❌ Error deleting synced records:`, error);
    }
}

// Get CSRF token
function getCSRFToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find((row) => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue || '';
}

// Sync function for apartments
async function syncApartments(pending) {
    for (const item of pending) {
        try {
            const { action, tempId, ...data } = item;
            let url = '/accounts/apartments/create/';
            let method = 'POST';

            if (action === 'update' && data.id) {
                url = `/accounts/apartments/update/${data.id}/`;
                method = 'POST';
            } else if (action === 'delete' && data.id) {
                url = `/accounts/apartments/delete/${data.id}/`;
                method = 'POST';
                data._method = 'DELETE';
            }

            const response = await fetch(url, {
                method,
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                },
                body: JSON.stringify(data),
            });

            if (response.ok) {
                await markSynced(STORES.APARTMENTS, tempId);
                console.log(`✅ Synced apartment: ${data.name || data.id}`);
            } else {
                console.error(`❌ Failed to sync apartment:`, await response.text());
            }
        } catch (error) {
            console.error(`⚠️ Error syncing apartment:`, error);
        }
    }
}

// Sync function for tenants
async function syncTenants(pending) {
    for (const item of pending) {
        try {
            const { action, tempId, ...data } = item;
            let url = '/accounts/tenants/create/';
            let method = 'POST';

            if (action === 'update' && data.id) {
                url = `/accounts/tenants/update/${data.id}/`;
                method = 'POST';
            } else if (action === 'delete' && data.id) {
                url = `/accounts/tenants/delete/${data.id}/`;
                method = 'POST';
            }

            const formData = new FormData();
            Object.keys(data).forEach((key) => {
                if (data[key] !== null && data[key] !== undefined) {
                    formData.append(key, data[key]);
                }
            });

            const response = await fetch(url, {
                method,
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                },
                body: formData,
            });

            if (response.ok) {
                await markSynced(STORES.TENANTS, tempId);
                console.log(`✅ Synced tenant: ${data.first_name} ${data.last_name}`);
            } else {
                console.error(`❌ Failed to sync tenant:`, await response.text());
            }
        } catch (error) {
            console.error(`⚠️ Error syncing tenant:`, error);
        }
    }
}

// Sync function for payments
async function syncPayments(pending) {
    for (const item of pending) {
        try {
            const { action, tempId, ...data } = item;
            let url = '/accounts/payments/create/';
            let method = 'POST';

            if (action === 'update' && data.id) {
                url = `/accounts/payments/${data.id}/edit/`;
                method = 'POST';
            } else if (action === 'delete' && data.id) {
                url = `/accounts/payments/${data.id}/delete/`;
                method = 'POST';
            }

            const formData = new FormData();
            Object.keys(data).forEach((key) => {
                if (data[key] !== null && data[key] !== undefined) {
                    formData.append(key, data[key]);
                }
            });

            const response = await fetch(url, {
                method,
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                },
                body: formData,
            });

            if (response.ok) {
                await markSynced(STORES.PAYMENTS, tempId);
                console.log(`✅ Synced payment: ${data.id || tempId}`);
            } else {
                console.error(`❌ Failed to sync payment:`, await response.text());
            }
        } catch (error) {
            console.error(`⚠️ Error syncing payment:`, error);
        }
    }
}

// Sync function for bills
async function syncBills(pending) {
    for (const item of pending) {
        try {
            const { action, tempId, ...data } = item;
            let url = '/accounts/bills/create/';
            let method = 'POST';

            if (action === 'update' && data.id) {
                url = `/accounts/bills/update/${data.id}/`;
                method = 'POST';
            } else if (action === 'delete' && data.id) {
                url = `/accounts/bills/delete/${data.id}/`;
                method = 'POST';
            }

            const formData = new FormData();
            Object.keys(data).forEach((key) => {
                if (data[key] !== null && data[key] !== undefined) {
                    formData.append(key, data[key]);
                }
            });

            const response = await fetch(url, {
                method,
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                },
                body: formData,
            });

            if (response.ok) {
                await markSynced(STORES.BILLS, tempId);
                console.log(`✅ Synced bill: ${data.id || tempId}`);
            } else {
                console.error(`❌ Failed to sync bill:`, await response.text());
            }
        } catch (error) {
            console.error(`⚠️ Error syncing bill:`, error);
        }
    }
}

// Sync function for other charges
async function syncOtherCharges(pending) {
    for (const item of pending) {
        try {
            const { action, tempId, ...data } = item;
            let url = '/accounts/other-charges/create/';
            let method = 'POST';

            if (action === 'update' && data.id) {
                url = `/accounts/other-charges/update/${data.id}/`;
                method = 'POST';
            } else if (action === 'delete' && data.id) {
                url = `/accounts/other-charges/delete/${data.id}/`;
                method = 'POST';
            }

            const formData = new FormData();
            Object.keys(data).forEach((key) => {
                if (data[key] !== null && data[key] !== undefined) {
                    formData.append(key, data[key]);
                }
            });

            const response = await fetch(url, {
                method,
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                },
                body: formData,
            });

            if (response.ok) {
                await markSynced(STORES.OTHER_CHARGES, tempId);
                console.log(`✅ Synced other charge: ${data.name || data.id}`);
            } else {
                console.error(`❌ Failed to sync other charge:`, await response.text());
            }
        } catch (error) {
            console.error(`⚠️ Error syncing other charge:`, error);
        }
    }
}

// Main sync function - syncs all pending data
async function syncWhenOnline() {
    if (!navigator.onLine) {
        console.log('⚠️ Device is offline, cannot sync');
        return;
    }

    console.log('🌐 Starting sync of offline data...');
    const pending = await getAllPending();

    // Sync each data type
    if (pending.APARTMENTS && pending.APARTMENTS.length > 0) {
        await syncApartments(pending.APARTMENTS);
    }
    if (pending.TENANTS && pending.TENANTS.length > 0) {
        await syncTenants(pending.TENANTS);
    }
    if (pending.PAYMENTS && pending.PAYMENTS.length > 0) {
        await syncPayments(pending.PAYMENTS);
    }
    if (pending.BILLS && pending.BILLS.length > 0) {
        await syncBills(pending.BILLS);
    }
    if (pending.OTHER_CHARGES && pending.OTHER_CHARGES.length > 0) {
        await syncOtherCharges(pending.OTHER_CHARGES);
    }

    // Clean up synced records
    Object.values(STORES).forEach(async (storeName) => {
        await deleteSynced(storeName);
    });

    // Update UI
    updateOfflineIndicator();
    
    // Reload page if there was data to sync
    const totalPending = Object.values(pending).reduce((sum, arr) => sum + arr.length, 0);
    if (totalPending > 0) {
        console.log(`✅ Sync complete. Reloading page...`);
        setTimeout(() => window.location.reload(), 1000);
    } else {
        console.log('✅ No pending data to sync');
    }
}

// Update offline indicator
function updateOfflineIndicator() {
    getAllPending().then((pending) => {
        const totalPending = Object.values(pending).reduce((sum, arr) => sum + arr.length, 0);
        const indicator = document.getElementById('offline-indicator');
        if (indicator) {
            if (totalPending > 0) {
                indicator.textContent = `⚠️ ${totalPending} item(s) pending sync`;
                indicator.style.display = 'block';
            } else if (!navigator.onLine) {
                indicator.textContent = '⚠️ You are offline';
                indicator.style.display = 'block';
            } else {
                indicator.style.display = 'none';
            }
        }
    });
}

// Legacy function for backward compatibility
function savePending(apartment) {
    return saveOffline(STORES.APARTMENTS, apartment, 'create');
}

// Auto-sync when coming back online
window.addEventListener('online', () => {
    console.log('🌐 Connection restored, syncing offline data...');
    syncWhenOnline();
});

// Listen for service worker messages
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.addEventListener('message', (event) => {
        if (event.data && event.data.type === 'SYNC_OFFLINE_DATA') {
            syncWhenOnline();
        }
    });
}

// Export functions for use in other scripts
window.ApartmentDB = {
    saveOffline,
    getPending,
    getAllPending,
    syncWhenOnline,
    STORES,
    savePending // Legacy support
};
