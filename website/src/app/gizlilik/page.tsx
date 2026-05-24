import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";

export default function Gizlilik() {
  return (
    <main className="min-h-screen bg-background text-primary">
      <Navbar />
      <div className="container mx-auto px-6 py-12 max-w-4xl">
        <Link href="/" className="inline-flex items-center gap-2 text-sm text-accent hover:text-accent/80 transition-colors mb-8">
          <ArrowLeft className="w-4 h-4" />
          Ana Sayfaya Dön
        </Link>
        <h1 className="text-3xl font-bold text-primary mb-6">Gizlilik Politikası (KVKK Aydınlatma Metni)</h1>
        
        <div className="max-w-none text-secondary space-y-6 leading-relaxed">
          <p>
            RouteDesk ("Şirket", "Biz", "Bizi" veya "Bize"), gizliliğinize büyük önem vermektedir. Bu Gizlilik Politikası, masaüstü terminal yönetim yazılımımız ve web sitemiz aracılığıyla sağladığınız kişisel verilerin 6698 sayılı Kişisel Verilerin Korunması Kanunu ("KVKK") kapsamında nasıl işlendiğini açıklamaktadır.
          </p>
          
          <h2 className="text-xl font-bold text-primary mt-8 mb-4">1. Toplanan Veriler</h2>
          <p>
            Uygulama üzerinden toplanan kişisel veriler, temel olarak ulaşım operasyonlarının yürütülmesi amacıyla işlenir. Ad, soyad, telefon numarası ve bilet rezervasyon kayıtlarınız gibi veriler; size, firmanıza veya yolcularınıza ait güvenli operasyon süreci sağlamak içindir. Masaüstü uygulamamız, verileri temel olarak yerel veritabanınızda (SQLite) depolar.
          </p>

          <h2 className="text-xl font-bold text-primary mt-8 mb-4">2. Verilerin Kullanım Amacı</h2>
          <p>
            Toplanan bilgiler, terminal yönetim işlemlerinin (bilet kesimi, peron takibi, sefer planlaması) gerçekleştirilmesi, yasal yükümlülüklerin yerine getirilmesi (Karayolu Taşıma Yönetmeliği vb.) ve müşteri memnuniyetinin sağlanması amacıyla kullanılmaktadır.
          </p>

          <h2 className="text-xl font-bold text-primary mt-8 mb-4">3. Veri Güvenliği</h2>
          <p>
            Kişisel verileriniz, uygun güvenlik düzeyini temin etmeye yönelik her türlü idari ve teknik tedbir alınarak korunmaktadır. Yazılımımız, yetkisiz erişimi engellemek adına operatör giriş sistemi ve şifreleme yöntemleri kullanmaktadır.
          </p>

          <h2 className="text-xl font-bold text-primary mt-8 mb-4">4. Haklarınız</h2>
          <p>
            KVKK'nın 11. maddesi uyarınca veri sorumlusuna başvurarak; kişisel verilerinizin işlenip işlenmediğini öğrenme, işlenmişse bilgi talep etme, işlenme amacını ve amacına uygun kullanılıp kullanılmadığını öğrenme, eksik veya yanlış işlenmiş olması hâlinde bunların düzeltilmesini isteme haklarına sahipsiniz.
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
