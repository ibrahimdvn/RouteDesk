"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { BusFront, Eye, EyeOff, Loader2, ShieldAlert } from "lucide-react";

export default function AdminLogin() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPass, setShowPass] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await fetch("/api/admin/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      if (res.ok) {
        router.push("/admin");
        router.refresh();
      } else {
        const data = await res.json();
        setError(data.message || "Geçersiz bilgiler.");
      }
    } catch {
      setError("Bir hata oluştu. Lütfen tekrar deneyin.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <div className="w-full max-w-sm">
        {/* Logo */}
        <div className="flex flex-col items-center mb-8">
          <div className="w-14 h-14 rounded-2xl bg-red-600 flex items-center justify-center mb-4 shadow-lg shadow-red-600/20">
            <BusFront className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-xl font-bold text-primary">RouteDesk Admin</h1>
          <p className="text-sm text-secondary mt-1">Yönetim Merkezine Giriş</p>
        </div>

        {/* Card */}
        <div className="bg-card border border-border rounded-xl p-6 shadow-2xl">
          <div className="flex items-center gap-2 text-xs text-secondary bg-background border border-border rounded-lg px-3 py-2 mb-6">
            <ShieldAlert className="w-3.5 h-3.5 text-yellow-500 shrink-0" />
            <span>Bu alan yalnızca yetkili yöneticilere açıktır.</span>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-1.5">
              <label className="text-xs font-medium text-secondary">Kullanıcı Adı</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                autoFocus
                autoComplete="username"
                className="w-full bg-background border border-border rounded-md px-3 py-2.5 text-sm text-primary focus:outline-none focus:border-accent transition-colors"
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-medium text-secondary">Şifre</label>
              <div className="relative">
                <input
                  type={showPass ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  autoComplete="current-password"
                  className="w-full bg-background border border-border rounded-md px-3 py-2.5 pr-10 text-sm text-primary focus:outline-none focus:border-accent transition-colors"
                />
                <button
                  type="button"
                  onClick={() => setShowPass(!showPass)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-secondary hover:text-primary transition-colors"
                >
                  {showPass ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            {error && (
              <div className="text-red-400 text-xs bg-red-500/10 border border-red-500/20 rounded-md px-3 py-2">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-accent hover:bg-accent/90 text-white font-medium py-2.5 rounded-md transition-colors flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed mt-2"
            >
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : null}
              {loading ? "Doğrulanıyor..." : "Giriş Yap"}
            </button>
          </form>
        </div>

        <p className="text-center text-xs text-secondary/50 mt-6">
          RouteDesk Yönetim Merkezi &copy; {new Date().getFullYear()}
        </p>
      </div>
    </div>
  );
}
