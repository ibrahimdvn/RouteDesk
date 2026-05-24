const Database = require('better-sqlite3');
const path = require('path');

try {
    const dbPath = path.join(process.cwd(), '../routedesk.db');
    console.log("DB Path:", dbPath);
    const db = new Database(dbPath, { fileMustExist: true });
    const trips = db.prepare("SELECT * FROM trips").all();
    console.log("Trips:", trips);
} catch (err) {
    console.error("Error:", err);
}
