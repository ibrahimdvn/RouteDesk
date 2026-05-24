import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";

export default function CerezPolitikasi() {
  return (
    <main className="min-h-screen bg-background text-primary">
      <Navbar />
      <div className="container mx-auto px-6 py-12 max-w-4xl">
        <Link href="/" className="inline-flex items-center gap-2 text-sm text-accent hover:text-accent/80 transition-colors mb-8">
          <ArrowLeft className="w-4 h-4" />
          Ana Sayfaya Dön
        </Link>
        <h1 className="text-3xl font-bold text-primary mb-6">Çerez (Cookie) Politikası</h1>
        
        <div className="max-w-none text-secondary space-y-6 leading-relaxed">
          <p>
            RouteDesk ("Biz", "Bizi" veya "Bize") olarak, web sitemizi ziyaret ettiğinizde deneyiminizi geliştirmek, site trafiğini analiz etmek ve size daha iyi hizmet sunabilmek amacıyla çerezler (cookies) kullanmaktayız.
          </p>
          
          <h2 className="text-xl font-bold text-primary mt-8 mb-4">1. Çerez Nedir?</h2>
          <p>
            Çerezler, bir web sitesini ziyaret ettiğinizde cihazınıza (bilgisayar, tablet, akıllı telefon) kaydedilen küçük metin dosyalarıdır. Bu dosyalar, siteyi kullanımınız hakkında bilgileri saklayarak bir sonraki ziyaretinizde sizi tanımamızı ve siteyi size göre optimize etmemizi sağlar.
          </p>

          <h2 className="text-xl font-bold text-primary mt-8 mb-4">2. Kullandığımız Çerez Türleri</h2>
          <ul className="list-disc pl-6 space-y-2">
            <li><strong>Zorunlu Çerezler:</strong> Web sitemizin temel işlevlerinin (gezinme, form gönderimi vb.) çalışması için kesinlikle gereklidir. Bu çerezler kapatılamaz.</li>
            <li><strong>Analitik Çerezler:</strong> Ziyaretçilerin web sitesiyle nasıl etkileşime girdiğini anlamamıza yardımcı olur. Ziyaretçi sayısı, hemen çıkma oranı gibi metrikleri ölçer.</li>
            <li><strong>İşlevsel Çerezler:</strong> Dil tercihiniz gibi seçimlerinizi hatırlayarak size kişiselleştirilmiş bir deneyim sunar.</li>
          </ul>

          <h2 className="text-xl font-bold text-primary mt-8 mb-4">3. Çerezlerin Yönetimi</h2>
          <p>
            Çerezlerin cihazınıza kaydedilmesini istemiyorsanız, tarayıcı ayarlarınızı değiştirerek çerezleri reddedebilir veya silebilirsiniz. Ancak, çerezleri tamamen devre dışı bırakmanın web sitemizin bazı özelliklerinin düzgün çalışmasını engelleyebileceğini lütfen unutmayın.
          </p>
          <p>En popüler tarayıcılarda çerezleri nasıl yöneteceğinizi öğrenmek için tarayıcınızın "Yardım" menüsünü inceleyebilirsiniz.</p>

          <p className="mt-12 text-sm text-border">
            Son Güncelleme: {new Date().toLocaleDateString('tr-TR')}
          </p>
        </div>
      </div>
      <Footer />
    </main>
  );
}
