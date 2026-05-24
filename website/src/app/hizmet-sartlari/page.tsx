import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";

export default function HizmetSartlari() {
  return (
    <main className="min-h-screen bg-background text-primary">
      <Navbar />
      <div className="container mx-auto px-6 py-12 max-w-4xl">
        <Link href="/" className="inline-flex items-center gap-2 text-sm text-accent hover:text-accent/80 transition-colors mb-8">
          <ArrowLeft className="w-4 h-4" />
          Ana Sayfaya Dön
        </Link>
        <h1 className="text-3xl font-bold text-primary mb-6">Hizmet Şartları</h1>
        
        <div className="max-w-none text-secondary space-y-6 leading-relaxed">
          <p>
            Lütfen RouteDesk yazılımını ve web sitesini kullanmadan önce bu hizmet şartlarını dikkatlice okuyunuz. RouteDesk'e erişerek veya kullanarak, bu şartlara bağlı kalmayı kabul etmiş sayılırsınız.
          </p>
          
          <h2 className="text-xl font-bold text-primary mt-8 mb-4">1. Lisans ve Kullanım</h2>
          <p>
            Size sağlanan RouteDesk yazılımı, satılmaz; yalnızca belirli şartlar altında lisanslanır. Bu lisans, yazılımı satın aldığınız pakete (Başlangıç, İşletme, Kurumsal) uygun olarak, yalnızca yetkili terminallerde kullanmanıza izin verir. Yazılımın kaynak kodlarının kopyalanması, tersine mühendislik yapılması veya izinsiz dağıtılması yasaktır.
          </p>

          <h2 className="text-xl font-bold text-primary mt-8 mb-4">2. Yasal Sorumluluk</h2>
          <p>
            Kullanıcı, RouteDesk üzerinden gerçekleştirdiği bilet satışları, müşteri kayıtları ve finansal işlemlerden kendisi sorumludur. RouteDesk, ulaştırma mevzuatına (Karayolu Taşıma Kanunu vb.) uyumunuz konusunda yasal bir taahhüt vermez; yazılım sadece süreçlerinizi yönetmek için bir araçtır.
          </p>

          <h2 className="text-xl font-bold text-primary mt-8 mb-4">3. Hizmet Sürekliliği</h2>
          <p>
            RouteDesk masaüstü uygulaması temel olarak yerel donanımınızda çalışır (Offline Support). Bu sebeple cihazınızın donanımsal arızalarından, işletim sistemi çökmelerinden veya yerel veritabanı (SQLite) silinmelerinden kaynaklanan veri kayıplarında RouteDesk sorumlu tutulamaz. Verilerin periyodik yedeğinin alınması kullanıcının sorumluluğundadır.
          </p>

          <h2 className="text-xl font-bold text-primary mt-8 mb-4">4. Fesih</h2>
          <p>
            Bu şartların ihlal edilmesi durumunda, RouteDesk yazılım lisansınızı askıya alma veya tamamen feshetme hakkını saklı tutar.
          </p>

          <p className="mt-12 text-sm text-border">
            Son Güncelleme: {new Date().toLocaleDateString('tr-TR')}
          </p>
        </div>
      </div>
      <Footer />
    </main>
  );
}
