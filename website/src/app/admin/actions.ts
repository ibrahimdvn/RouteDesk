"use server";

import { getDb, Trip, Ticket } from "@/lib/db";
import { revalidatePath } from "next/cache";

export async function getTrips(): Promise<Trip[]> {
  try {
    const db = getDb();
    const rows = db.prepare("SELECT * FROM trips ORDER BY departure ASC").all() as Trip[];
    db.close();
    return rows;
  } catch (error) {
    console.error("Error fetching trips:", error);
    return [];
  }
}

export async function deleteTrip(id: number) {
  try {
    const db = getDb();
    const trip = db.prepare("SELECT code FROM trips WHERE id = ?").get(id) as { code: string };
    if (trip) {
      db.prepare("DELETE FROM tickets WHERE trip_code = ?").run(trip.code);
    }
    db.prepare("DELETE FROM trips WHERE id = ?").run(id);
    db.close();
    revalidatePath("/admin");
    return { success: true };
  } catch (error) {
    console.error("Error deleting trip:", error);
    return { success: false };
  }
}

export async function updateTripStatus(id: number, status: string) {
  try {
    const db = getDb();
    db.prepare("UPDATE trips SET status = ? WHERE id = ?").run(status, id);
    db.close();
    revalidatePath("/admin");
    return { success: true };
  } catch (error) {
    console.error("Error updating trip:", error);
    return { success: false };
  }
}

export async function getTickets(): Promise<Ticket[]> {
  try {
    const db = getDb();
    const rows = db.prepare(`
      SELECT tickets.*, trips.route, trips.departure 
      FROM tickets 
      LEFT JOIN trips ON tickets.trip_code = trips.code 
      ORDER BY tickets.id DESC LIMIT 100
    `).all() as any[];
    db.close();
    return rows;
  } catch (error) {
    console.error("Error fetching tickets:", error);
    return [];
  }
}

export async function deleteTicket(id: number) {
  try {
    const db = getDb();
    
    // Masaüstü uygulamasındaki doluluk (occupancy) hesaplamasını etkileyebileceğinden, 
    // bilet silindiğinde trip occupancy otomatik düzeltilmeyebilir. Ancak masaüstü zaten
    // bilet tablosundan hesaplama yapıyorsa sorun olmaz. Biz sadece bileti silelim.
    db.prepare("DELETE FROM tickets WHERE id = ?").run(id);
    db.close();
    
    revalidatePath("/admin");
    return { success: true };
  } catch (error) {
    console.error("Error deleting ticket:", error);
    return { success: false };
  }
}

export async function getOperators() {
  try {
    const db = getDb();
    const rows = db.prepare("SELECT id, username, full_name FROM operators ORDER BY id DESC").all();
    db.close();
    return rows;
  } catch (error) {
    console.error("Error fetching operators:", error);
    return [];
  }
}

export async function getMaintenanceMode(): Promise<boolean> {
  try {
    const db = getDb();
    db.prepare("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)").run();
    const row = db.prepare("SELECT value FROM settings WHERE key='maintenance_mode'").get() as { value: string } | undefined;
    db.close();
    return row?.value === "true";
  } catch (error) {
    console.error("Error fetching maintenance mode:", error);
    return false;
  }
}

export async function toggleMaintenanceMode(isMaintenance: boolean) {
  try {
    const db = getDb();
    db.prepare("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)").run();
    db.prepare("INSERT OR REPLACE INTO settings (key, value) VALUES ('maintenance_mode', ?)").run(isMaintenance ? "true" : "false");
    db.close();
    revalidatePath("/admin");
    return { success: true };
  } catch (error) {
    console.error("Error toggling maintenance mode:", error);
    return { success: false };
  }
}

export async function deleteOperator(id: number) {
  try {
    const db = getDb();
    db.prepare("DELETE FROM operators WHERE id = ?").run(id);
    const maxIdRes = db.prepare("SELECT MAX(id) as maxId FROM operators").get() as { maxId: number | null };
    const maxId = maxIdRes.maxId || 0;
    try {
      db.prepare("UPDATE sqlite_sequence SET seq = ? WHERE name = 'operators'").run(maxId);
    } catch (_) {}
    db.close();
    revalidatePath("/admin");
    return { success: true };
  } catch (error) {
    console.error("Error deleting operator:", error);
    return { success: false };
  }
}

export async function getCustomers() {
  try {
    const db = getDb();
    const rows = db.prepare("SELECT phone, name, tc_no FROM customers ORDER BY name ASC").all();
    db.close();
    return rows;
  } catch (error) {
    console.error("Error fetching customers:", error);
    return [];
  }
}

export async function deleteCustomer(phone: string) {
  try {
    const db = getDb();
    db.prepare("DELETE FROM customers WHERE phone = ?").run(phone);
    db.close();
    revalidatePath("/admin");
    return { success: true };
  } catch (error) {
    console.error("Error deleting customer:", error);
    return { success: false };
  }
}
