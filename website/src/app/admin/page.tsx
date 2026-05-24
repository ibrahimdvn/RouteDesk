import { getTrips, getTickets, getOperators, getMaintenanceMode, getCustomers } from "./actions";
import AdminClient from "./AdminClient";
import type { Metadata } from "next";

export const dynamic = "force-dynamic";
export const revalidate = 0;

export const metadata: Metadata = {
  title: "RouteDesk Admin | Yönetim Merkezi",
  icons: {
    icon: [
      { url: "/favicon.ico", sizes: "any" },
      { url: "/icon.png", type: "image/png" },
    ],
    shortcut: "/favicon.ico",
  },
};

export default async function AdminPage() {
  const initialTrips = await getTrips();
  const initialTickets = await getTickets();
  const initialOperators = await getOperators();
  const initialMaintenanceMode = await getMaintenanceMode();
  const initialCustomers = await getCustomers();

  return (
    <AdminClient 
      initialTrips={initialTrips} 
      initialTickets={initialTickets} 
      initialOperators={initialOperators as any[]}
      initialMaintenanceMode={initialMaintenanceMode}
      initialCustomers={initialCustomers as any[]}
    />
  );
}
