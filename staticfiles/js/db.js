const dbName = "apartment_offline_db";
const dbVersion = 2; // bump version to recreate correctly
let db;

function openDB() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open(dbName, dbVersion);

        request.onupgradeneeded = (event) => {
            db = event.target.result;
            if (!db.objectStoreNames.contains("pending_changes")) {
                db.createObjectStore("pending_changes", { keyPath: "id", autoIncrement: true });
            }
        };

        request.onsuccess = (event) => {
            db = event.target.result;
            resolve(db);
        };

        request.onerror = (event) => {
            reject(event.target.error);
        };
    });
}

async function saveOffline(data) {
    const db = await openDB();
    const tx = db.transaction("pending_changes", "readwrite");
    tx.objectStore("pending_changes").add(data);
    tx.oncomplete = () => console.log("✅ Data saved offline:", data);
    tx.onerror = (e) => console.error("❌ Failed to save offline:", e);
}

async function getAllPending() {
    const db = await openDB();
    const tx = db.transaction("pending_changes", "readonly");
    const store = tx.objectStore("pending_changes");
    return new Promise((resolve) => {
        const req = store.getAll();
        req.onsuccess = () => resolve(req.result);
    });
}

async function syncWhenOnline() {
    const pending = await getAllPending();
    if (pending.length > 0) {
        console.log("🔄 Syncing offline data:", pending);
        // later we’ll send to Django here
    }
}

window.addEventListener("online", syncWhenOnline);
