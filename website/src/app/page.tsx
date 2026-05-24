import Navbar from "@/components/Navbar";
import HeroSection from "@/components/HeroSection";
import FeaturesSection from "@/components/FeaturesSection";
import ShowcaseSection from "@/components/ShowcaseSection";
import SeatLayoutSection from "@/components/SeatLayoutSection";
import WorkflowSection from "@/components/WorkflowSection";
import WhyRouteDeskSection from "@/components/WhyRouteDeskSection";
import UseCasesSection from "@/components/UseCasesSection";
import PricingSection from "@/components/PricingSection";
import ContactSection from "@/components/ContactSection";
import Footer from "@/components/Footer";

export default function Home() {
  return (
    <main className="min-h-screen bg-background text-primary">
      <Navbar />
      <HeroSection />
      <FeaturesSection />
      <ShowcaseSection />
      <SeatLayoutSection />
      <WorkflowSection />
      <WhyRouteDeskSection />
      <UseCasesSection />
      <PricingSection />
      <ContactSection />
      <Footer />
    </main>
  );
}
