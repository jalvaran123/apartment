// ----------------------
// IndexedDB Config
// ----------------------
const DB_NAME = "apartmentDB_v3"; // new version for clean reset
const DB_VERSION = 3;

// ----------------------
// Open IndexedDB
// ----------------------
let openDB = indexedDB.open(DB_NAME, DB_VERSION);

openDB.onupgradeneeded = (event) => {
    const db = event.target.result;
    // create object store if it doesn't exist
    if (!db.objectStoreNames.contains("pendingApartments")) {
        db.createObjectStore("pendingApartments", { keyPath: "id", autoIncrement: true });
        console.log("✅ Created store: pendingApartments");
    }
};

openDB.onerror = (event) => {
    console.error("❌ Failed to open DB:", event.target.error);
};

// ----------------------
// Save Offline
// ----------------------
function savePending(apartment) {
    const request = indexedDB.open(DB_NAME, DB_VERSION);
    request.onsuccess = (event) => {
        const db = event.target.result;
        const tx = db.transaction("pendingApartments", "readwrite");
        const store = tx.objectStore("pendingApartments");
        store.add(apartment);
        console.log("💾 Saved offline:", apartment);
    };
    request.onerror = (event) => {
        console.error("❌ IndexedDB error:", event.target.error);
    };
}

// ----------------------
// Get All Pending Data
// ----------------------
function getAllPending() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open(DB_NAME, DB_VERSION);
        request.onsuccess = (event) => {
            const db = event.target.result;
            if (!db.objectStoreNames.contains("pendingApartments")) {
                console.error("⚠️ Object store not found, reloading DB...");
                db.close();
                indexedDB.deleteDatabase(DB_NAME);
                reject("Store not found");
                return;
            }
            const tx = db.transaction("pendingApartments", "readonly");
            const store = tx.objectStore("pendingApartments");
            const getReq = store.getAll();
            getReq.onsuccess = () => resolve(getReq.result);
            getReq.onerror = (err) => reject(err);
        };
    });
}

// ----------------------
// Clear Store
// ----------------------
function clearPending() {
    const request = indexedDB.open(DB_NAME, DB_VERSION);
    request.onsuccess = (event) => {
        const db = event.target.result;
        const tx = db.transaction("pendingApartments", "readwrite");
        tx.objectStore("pendingApartments").clear();
        console.log("🧹 Cleared all pending apartments");
    };
}

// ----------------------
// Get CSRF Token
// ----------------------
function getCSRFToken() {
    const cookieValue = document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue || '';
}

// ----------------------
// Sync to Server (Main Sync Function)
// ----------------------
async function syncWhenOnline() {
    const pending = await getAllPending().catch((err) => {
        console.error("Sync aborted:", err);
        return [];
    });

    if (pending.length === 0) {
        console.log("✅ No pending data to sync.");
        return;
    }

    console.log(`🌐 Syncing ${pending.length} offline entries to server...`);

    for (const apartment of pending) {
        try {
            const res = await fetch("/accounts/apartments/sync/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(),
                },
                body: JSON.stringify(apartment),
            });

            if (res.ok) {
                const result = await res.json();
                console.log("✅ Synced:", apartment.name, result);
            } else {
                console.error("❌ Failed to sync:", await res.text());
            }
        } catch (err) {
            console.error("⚠️ Network error syncing:", err);
        }
    }

    // Clear after successful sync
    clearPending();
}

// ----------------------
// Auto Sync When Online
// ----------------------
window.addEventListener("online", syncWhenOnline);
