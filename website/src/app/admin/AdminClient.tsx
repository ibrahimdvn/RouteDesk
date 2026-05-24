"use client";

import { Trip, Ticket, Operator } from "@/lib/db";
import { deleteTrip, updateTripStatus, deleteTicket, toggleMaintenanceMode, deleteOperator, deleteCustomer } from "./actions";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { Trash2, Edit2, BusFront, Ticket as TicketIcon, Loader2, ArrowLeft, Users, Settings, AlertTriangle, ShieldCheck, X, UserCircle, LogOut } from "lucide-react";
import Link from "next/link";

interface AdminClientProps {
  initialTrips: Trip[];
  initialTickets: any[];
  initialOperators: Operator[];
  initialMaintenanceMode: boolean;
  initialCustomers: any[];
}

export default function AdminClient({ initialTrips, initialTickets, initialOperators, initialMaintenanceMode, initialCustomers }: AdminClientProps) {
  const [activeTab, setActiveTab] = useState<"trips" | "tickets" | "customers" | "operators" | "maintenance">("trips");
  const [loadingAction, setLoadingAction] = useState<number | string | null>(null);
  const [isMaintenance, setIsMaintenance] = useState(initialMaintenanceMode);
  const router = useRouter();

  const handleLogout = async () => {
    await fetch("/api/admin/logout", { method: "POST" });
    router.push("/admin/login");
  };

  // Custom Modal State
  const [modal, setModal] = useState<{
    isOpen: boolean;
    title: string;
    message: string;
    type: "danger" | "warning" | "prompt";
    inputValue?: string;
    onConfirm: (val?: string) => void;
  }>({
    isOpen: false,
    title: "",
    message: "",
    type: "warning",
    inputValue: "",
    onConfirm: () => {}
  });

  const openModal = (title: string, message: string, type: "danger" | "warning" | "prompt", onConfirm: (val?: string) => void, initialInput: string = "") => {
    setModal({ isOpen: true, title, message, type, onConfirm, inputValue: initialInput });
  };

  const closeModal = () => setModal(prev => ({ ...prev, isOpen: false }));

  const handleDeleteTrip = (id: number) => {
    openModal(
      "Seferi Sil",
      "Bu seferi ve içindeki tüm biletleri silmek istediğinize emin misiniz? Bu işlem geri alınamaz.",
      "danger",
      async () => {
        closeModal();
        setLoadingAction(id);
        await deleteTrip(id);
        setLoadingAction(null);
      }
    );
  };

  const handleUpdateTrip = (id: number, currentStatus: string) => {
    openModal(
      "Sefer Durumunu Güncelle",
      "Yeni durumu girin (Planlandı, Yolcu Alımında, Rötarlı, İptal Edildi vs.):",
      "prompt",
      async (newStatus) => {
        if (!newStatus) {
          closeModal();
          return;
        }
        closeModal();
        setLoadingAction(id);
        await updateTripStatus(id, newStatus);
        setLoadingAction(null);
      },
      currentStatus
    );
  };

  const handleDeleteTicket = (id: number) => {
    openModal(
      "Bileti İptal Et",
      "Bu bileti iptal etmek istediğinize emin misiniz? Sistem veritabanından kalıcı olarak silinecektir.",
      "danger",
      async () => {
        closeModal();
        setLoadingAction(id);
        await deleteTicket(id);
        setLoadingAction(null);
      }
    );
  };

  const handleToggleMaintenance = () => {
    openModal(
      isMaintenance ? "Sistemi Çevrimiçi Yap" : "Sistem Bakım Modu",
      `Sistem bakım modunu ${isMaintenance ? 'kapatmak' : 'açmak'} istediğinize emin misiniz? Bakım modu açıkken operatörler masaüstü uygulamasına giriş yapamaz.`,
      "warning",
      async () => {
        closeModal();
        setLoadingAction('maintenance');
        const newState = !isMaintenance;
        const res = await toggleMaintenanceMode(newState);
        if (res.success) {
          setIsMaintenance(newState);
        }
        setLoadingAction(null);
      }
    );
  };

  return (
    <div className="min-h-screen bg-background text-primary">
      {/* Top Navbar */}
      <div className="border-b border-border bg-card">
        <div className="container mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/" className="text-secondary hover:text-primary transition-colors">
              <ArrowLeft className="w-5 h-5" />
            </Link>
            <div className="w-8 h-8 rounded-lg bg-red-600 flex items-center justify-center">
              <BusFront className="w-5 h-5 text-white" />
            </div>
            <span className="font-bold text-lg tracking-tight">RouteDesk Admin Merkezi</span>
          </div>
          <div className="text-sm font-medium flex items-center gap-3">
            {isMaintenance ? (
              <span className="flex items-center gap-1 text-yellow-500 bg-yellow-500/10 px-3 py-1 rounded-full text-xs">
                <AlertTriangle className="w-3.5 h-3.5" />
                Bakım Modu Aktif
              </span>
            ) : (
              <span className="flex items-center gap-1 text-green-500 bg-green-500/10 px-3 py-1 rounded-full text-xs">
                <ShieldCheck className="w-3.5 h-3.5" />
                Sistem Çevrimiçi
              </span>
            )}
            <span className="text-secondary">| Veritabanı: Canlı (SQLite)</span>
            <button
              onClick={handleLogout}
              className="flex items-center gap-1.5 text-xs text-secondary hover:text-red-400 transition-colors ml-2 border border-border hover:border-red-400/50 rounded px-2 py-1"
              title="Çıkış Yap"
            >
              <LogOut className="w-3.5 h-3.5" />
              Çıkış
            </button>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-6 py-8">
        <div className="flex flex-wrap gap-4 mb-8">
          <button 
            onClick={() => setActiveTab("trips")}
            className={`flex items-center gap-2 px-4 py-2 rounded-md font-medium transition-colors ${activeTab === "trips" ? "bg-accent text-white" : "bg-card border border-border text-secondary hover:bg-border/50"}`}
          >
            <BusFront className="w-4 h-4" /> Sefer Yönetimi
          </button>
          <button 
            onClick={() => setActiveTab("tickets")}
            className={`flex items-center gap-2 px-4 py-2 rounded-md font-medium transition-colors ${activeTab === "tickets" ? "bg-accent text-white" : "bg-card border border-border text-secondary hover:bg-border/50"}`}
          >
            <TicketIcon className="w-4 h-4" /> Bilet İptalleri
          </button>
          <button 
            onClick={() => setActiveTab("customers")}
            className={`flex items-center gap-2 px-4 py-2 rounded-md font-medium transition-colors ${activeTab === "customers" ? "bg-accent text-white" : "bg-card border border-border text-secondary hover:bg-border/50"}`}
          >
            <UserCircle className="w-4 h-4" /> Müşteriler
          </button>
          <button 
            onClick={() => setActiveTab("operators")}
            className={`flex items-center gap-2 px-4 py-2 rounded-md font-medium transition-colors ${activeTab === "operators" ? "bg-accent text-white" : "bg-card border border-border text-secondary hover:bg-border/50"}`}
          >
            <Users className="w-4 h-4" /> Operatörler
          </button>
          <button 
            onClick={() => setActiveTab("maintenance")}
            className={`flex items-center gap-2 px-4 py-2 rounded-md font-medium transition-colors ${activeTab === "maintenance" ? "bg-accent text-white" : "bg-card border border-border text-secondary hover:bg-border/50"}`}
          >
            <Settings className="w-4 h-4" /> Sistem Bakım
          </button>
        </div>

        {activeTab === "trips" && (
          <div className="bg-card border border-border rounded-lg overflow-hidden">
            <div className="p-4 border-b border-border flex justify-between items-center">
              <h2 className="font-bold text-lg">Tüm Seferler</h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm whitespace-nowrap">
                <thead className="bg-background text-secondary border-b border-border">
                  <tr>
                    <th className="p-4 font-medium">Saat</th>
                    <th className="p-4 font-medium">Firma</th>
                    <th className="p-4 font-medium">Kod</th>
                    <th className="p-4 font-medium">Güzergah</th>
                    <th className="p-4 font-medium">Şoför</th>
                    <th className="p-4 font-medium">Plaka</th>
                    <th className="p-4 font-medium">Peron</th>
                    <th className="p-4 font-medium">Fiyat</th>
                    <th className="p-4 font-medium">Doluluk</th>
                    <th className="p-4 font-medium">Durum</th>
                    <th className="p-4 font-medium text-right">İşlem</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {initialTrips.length === 0 ? (
                    <tr><td colSpan={11} className="p-4 text-center text-secondary">Sefer bulunamadı.</td></tr>
                  ) : initialTrips.map((trip) => (
                    <tr key={trip.id} className="hover:bg-border/20 transition-colors">
                      <td className="p-4">{trip.departure}</td>
                      <td className="p-4 text-secondary">{trip.company}</td>
                      <td className="p-4 font-medium">{trip.code}</td>
                      <td className="p-4">{trip.route}</td>
                      <td className="p-4 text-secondary">{trip.driver}</td>
                      <td className="p-4 text-secondary">{trip.plate}</td>
                      <td className="p-4 text-secondary">{trip.platform}</td>
                      <td className="p-4">{trip.price} ₺</td>
                      <td className="p-4">{trip.occupancy}</td>
                      <td className="p-4">
                        <span className="px-2 py-1 bg-border/50 rounded text-xs">{trip.status}</span>
                      </td>
                      <td className="p-4 text-right flex justify-end gap-2">
                        <button 
                          onClick={() => handleUpdateTrip(trip.id, trip.status)}
                          className="p-1.5 bg-blue-500/10 text-blue-500 hover:bg-blue-500/20 rounded transition-colors"
                          title="Durum Güncelle"
                        >
                          {loadingAction === trip.id ? <Loader2 className="w-4 h-4 animate-spin" /> : <Edit2 className="w-4 h-4" />}
                        </button>
                        <button 
                          onClick={() => handleDeleteTrip(trip.id)}
                          className="p-1.5 bg-red-500/10 text-red-500 hover:bg-red-500/20 rounded transition-colors"
                          title="Sil"
                        >
                          {loadingAction === trip.id ? <Loader2 className="w-4 h-4 animate-spin" /> : <Trash2 className="w-4 h-4" />}
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === "tickets" && (
          <div className="bg-card border border-border rounded-lg overflow-hidden">
            <div className="p-4 border-b border-border flex justify-between items-center">
              <h2 className="font-bold text-lg">Son Bilet Hareketleri</h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="bg-background text-secondary border-b border-border">
                  <tr>
                    <th className="p-4 font-medium">Yolcu Adı</th>
                    <th className="p-4 font-medium">TC Kimlik</th>
                    <th className="p-4 font-medium">Sefer Kodu</th>
                    <th className="p-4 font-medium">Koltuk</th>
                    <th className="p-4 font-medium">Fiyat</th>
                    <th className="p-4 font-medium text-right">Aksiyon</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {initialTickets.length === 0 ? (
                    <tr><td colSpan={6} className="p-4 text-center text-secondary">Bilet bulunamadı.</td></tr>
                  ) : initialTickets.map((ticket) => (
                    <tr key={ticket.id} className="hover:bg-border/20 transition-colors">
                      <td className="p-4 font-medium">{ticket.passenger_name}</td>
                      <td className="p-4 text-secondary">{ticket.tc_no}</td>
                      <td className="p-4">{ticket.trip_code} {ticket.route ? `(${ticket.route})` : ''}</td>
                      <td className="p-4 font-bold text-accent">{ticket.seat}</td>
                      <td className="p-4">{ticket.price} ₺</td>
                      <td className="p-4 text-right">
                        <button 
                          onClick={() => handleDeleteTicket(ticket.id)}
                          className="px-3 py-1.5 text-xs bg-red-500/10 text-red-500 hover:bg-red-500/20 rounded transition-colors flex items-center gap-2 ml-auto"
                        >
                          {loadingAction === ticket.id ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Trash2 className="w-3.5 h-3.5" />}
                          İptal Et
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === "customers" && (
          <div className="bg-card border border-border rounded-lg overflow-hidden">
            <div className="p-4 border-b border-border flex justify-between items-center">
              <h2 className="font-bold text-lg">Kayıtlı Müşteriler</h2>
              <span className="text-xs text-secondary bg-background border border-border px-2 py-1 rounded">{initialCustomers.length} kayıt</span>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="bg-background text-secondary border-b border-border">
                  <tr>
                    <th className="p-4 font-medium">Ad Soyad</th>
                    <th className="p-4 font-medium">TC Kimlik No</th>
                    <th className="p-4 font-medium">Telefon</th>
                    <th className="p-4 font-medium text-right">Aksiyon</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {initialCustomers.length === 0 ? (
                    <tr><td colSpan={4} className="p-4 text-center text-secondary">Müşteri bulunamadı.</td></tr>
                  ) : initialCustomers.map((customer) => (
                    <tr key={customer.phone} className="hover:bg-border/20 transition-colors">
                      <td className="p-4 font-medium flex items-center gap-3">
                        <div className="w-8 h-8 rounded-full bg-background border border-border flex items-center justify-center text-accent">
                          <UserCircle className="w-4 h-4" />
                        </div>
                        {customer.name}
                      </td>
                      <td className="p-4 text-secondary tracking-wider">{customer.tc_no}</td>
                      <td className="p-4">{customer.phone}</td>
                      <td className="p-4 text-right">
                        <button
                          onClick={() => openModal(
                            "Müşteriyi Sil",
                            `${customer.name} adlı müşteriyi kalıcı olarak silmek istediğinize emin misiniz?`,
                            "danger",
                            async () => {
                              closeModal();
                              setLoadingAction(customer.phone);
                              await deleteCustomer(customer.phone);
                              setLoadingAction(null);
                            }
                          )}
                          className="px-3 py-1.5 text-xs bg-red-500/10 text-red-500 hover:bg-red-500/20 rounded transition-colors flex items-center gap-2 ml-auto"
                        >
                          {loadingAction === customer.phone ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Trash2 className="w-3.5 h-3.5" />}
                          Sil
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === "operators" && (
          <div className="bg-card border border-border rounded-lg overflow-hidden">
            <div className="p-4 border-b border-border flex justify-between items-center">
              <h2 className="font-bold text-lg">Kayıtlı Operatörler</h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="bg-background text-secondary border-b border-border">
                  <tr>
                    <th className="p-4 font-medium w-24">Sıra / ID</th>
                    <th className="p-4 font-medium">Kullanıcı Adı (İsim Soyisim)</th>
                    <th className="p-4 font-medium text-right">Aksiyon</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {initialOperators.length === 0 ? (
                    <tr><td colSpan={3} className="p-4 text-center text-secondary">Operatör bulunamadı.</td></tr>
                  ) : initialOperators.map((operator, index) => (
                    <tr key={operator.id} className="hover:bg-border/20 transition-colors">
                      <td className="p-4 text-secondary">#{index + 1} <span className="text-xs opacity-50">(DB: {operator.id})</span></td>
                      <td className="p-4 font-medium flex items-center gap-3">
                        <div className="w-8 h-8 rounded bg-background border border-border flex items-center justify-center text-accent">
                          <Users className="w-4 h-4" />
                        </div>
                        {operator.username} <span className="text-secondary font-normal">({operator.full_name})</span>
                      </td>
                      <td className="p-4 text-right">
                        <button 
                          onClick={() => {
                            openModal(
                              "Operatörü Sil",
                              "Bu operatörü silmek istediğinize emin misiniz? Operatör veritabanından kalıcı olarak silinecektir.",
                              "danger",
                              async () => {
                                closeModal();
                                setLoadingAction(operator.id);
                                await deleteOperator(operator.id);
                                setLoadingAction(null);
                              }
                            );
                          }}
                          className="px-3 py-1.5 text-xs bg-red-500/10 text-red-500 hover:bg-red-500/20 rounded transition-colors flex items-center gap-2 ml-auto"
                        >
                          {loadingAction === operator.id ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Trash2 className="w-3.5 h-3.5" />}
                          Sil
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === "maintenance" && (
          <div className="bg-card border border-border rounded-lg overflow-hidden max-w-2xl">
            <div className="p-4 border-b border-border flex justify-between items-center">
              <h2 className="font-bold text-lg">Sistem Bakım Modu</h2>
            </div>
            <div className="p-6">
              <div className="flex items-start gap-4 mb-8">
                <div className={`w-12 h-12 rounded-lg flex items-center justify-center shrink-0 ${isMaintenance ? 'bg-yellow-500/20 text-yellow-500' : 'bg-background border border-border text-secondary'}`}>
                  <AlertTriangle className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="font-bold text-primary mb-1">Masaüstü Uygulaması Bağlantısı</h3>
                  <p className="text-sm text-secondary leading-relaxed">
                    Bakım modunu aktif ettiğinizde, masaüstü uygulaması tamamen erişime kapanır ve açılışta kullanıcılara "Sistem şu anda uzaktan bakım modundadır" uyarısı verir. Operatörler sisteme giriş yapamaz.
                  </p>
                </div>
              </div>
              
              <div className="bg-background border border-border rounded-lg p-4 flex items-center justify-between">
                <div>
                  <p className="font-medium text-primary mb-1">Mevcut Durum</p>
                  <p className={`text-sm font-bold ${isMaintenance ? 'text-yellow-500' : 'text-green-500'}`}>
                    {isMaintenance ? 'Bakım Modu Aktif (Uygulama Kapalı)' : 'Sistem Çevrimiçi (Uygulama Açık)'}
                  </p>
                </div>
                <button
                  onClick={handleToggleMaintenance}
                  disabled={loadingAction === 'maintenance'}
                  className={`px-4 py-2 rounded-md font-medium transition-colors flex items-center gap-2 ${
                    isMaintenance 
                      ? 'bg-green-600 hover:bg-green-700 text-white' 
                      : 'bg-yellow-600 hover:bg-yellow-700 text-white'
                  }`}
                >
                  {loadingAction === 'maintenance' && <Loader2 className="w-4 h-4 animate-spin" />}
                  {isMaintenance ? 'Sistemi Çevrimiçi Yap' : 'Bakım Modunu Başlat'}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Custom Confirmation/Prompt Modal */}
      {modal.isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-background/80 backdrop-blur-sm">
          <div className="bg-card border border-border rounded-xl shadow-2xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in-95 duration-200">
            <div className="flex justify-between items-center p-4 border-b border-border">
              <h3 className="font-bold text-lg flex items-center gap-2">
                {modal.type === "warning" ? (
                  <AlertTriangle className="w-5 h-5 text-yellow-500" />
                ) : modal.type === "danger" ? (
                  <AlertTriangle className="w-5 h-5 text-red-500" />
                ) : (
                  <Edit2 className="w-5 h-5 text-blue-500" />
                )}
                {modal.title}
              </h3>
              <button onClick={closeModal} className="text-secondary hover:text-primary transition-colors">
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="p-6">
              <p className="text-secondary leading-relaxed mb-4">
                {modal.message}
              </p>
              
              {modal.type === "prompt" && (
                <input 
                  type="text" 
                  value={modal.inputValue} 
                  onChange={(e) => setModal(prev => ({ ...prev, inputValue: e.target.value }))}
                  className="w-full bg-background border border-border rounded-md px-3 py-2 text-sm text-primary focus:outline-none focus:border-accent transition-colors" 
                  autoFocus
                />
              )}
            </div>
            
            <div className="p-4 border-t border-border bg-background flex justify-end gap-3">
              <button 
                onClick={closeModal}
                className="px-4 py-2 rounded-md text-sm font-medium border border-border bg-card text-primary hover:bg-border/50 transition-colors"
              >
                Vazgeç
              </button>
              <button 
                onClick={() => modal.onConfirm(modal.inputValue)}
                className={`px-4 py-2 rounded-md text-sm font-medium text-white transition-colors ${
                  modal.type === "warning" ? "bg-yellow-600 hover:bg-yellow-700" 
                  : modal.type === "danger" ? "bg-red-600 hover:bg-red-700"
                  : "bg-blue-600 hover:bg-blue-700"
                }`}
              >
                Onayla
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
