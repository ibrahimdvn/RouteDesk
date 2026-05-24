import Database from 'better-sqlite3';
import path from 'path';

// Veritabanı yolu: website klasörünün bir üst dizininde (RouteDesk/RouteDesk.db)
const dbPath = path.join(process.cwd(), '../RouteDesk.db');
console.log("Next.js SQLite Path:", dbPath);

export function getDb() {
  const db = new Database(dbPath, { readonly: false });
  return db;
}

export type Trip = {
  id: number;
  code: string;
  company: string;
  route: string;
  departure: string;
  arrival: string;
  driver: string;
  plate: string;
  platform: string;
  price: number;
  occupancy: string;
  status: string;
  total_seats: number;
  layout: string;
};

export type Ticket = {
  id: number;
  trip_code: string;
  seat: string;
  passenger_name: string;
  tc_no: string;
  price: number;
  route?: string; // from join
  departure?: string; // from join
};

export type Operator = {
  id: number;
  username: string;
  full_name: string;
};
