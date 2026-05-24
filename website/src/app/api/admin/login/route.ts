import { NextRequest, NextResponse } from "next/server";
import crypto from "crypto";

// Pre-hashed values for admin_1 and Aslandur1881_
const ADMIN_USERNAME_HASH = process.env.ADMIN_USERNAME_HASH ?? "fa0fdd6f1c979d680cd19cd9a6c7b78cd1422ff0864f2de7e33d2798676723db";
const ADMIN_PASSWORD_HASH = process.env.ADMIN_PASSWORD_HASH ?? "67a55c9676849de8857530441f4e67fd2690b9e7f9c0e30a5d173189cf2e0262";

// ── In-memory Rate Limiter ─────────────────────────────────────────────────
// Max 5 failed attempts per IP within 15 minutes → lockout
const failedAttempts = new Map<string, { count: number; lockedUntil: number }>();

const MAX_ATTEMPTS = 5;
const LOCKOUT_MS = 15 * 60 * 1000; // 15 dakika

function getClientIp(req: NextRequest): string {
  return (
    req.headers.get("x-forwarded-for")?.split(",")[0].trim() ??
    req.headers.get("x-real-ip") ??
    "unknown"
  );
}

function isRateLimited(ip: string): boolean {
  const record = failedAttempts.get(ip);
  if (!record) return false;
  if (record.lockedUntil > Date.now()) return true;
  // Kilit süresi geçtiyse sıfırla
  failedAttempts.delete(ip);
  return false;
}

function recordFailure(ip: string): void {
  const now = Date.now();
  const record = failedAttempts.get(ip) ?? { count: 0, lockedUntil: 0 };
  record.count += 1;
  if (record.count >= MAX_ATTEMPTS) {
    record.lockedUntil = now + LOCKOUT_MS;
  }
  failedAttempts.set(ip, record);
}

function clearFailures(ip: string): void {
  failedAttempts.delete(ip);
}
// ───────────────────────────────────────────────────────────────────────────

export async function POST(req: NextRequest) {
  const ip = getClientIp(req);

  // Rate limit kontrolü
  if (isRateLimited(ip)) {
    return NextResponse.json(
      { success: false, message: "Çok fazla başarısız giriş denemesi. 15 dakika sonra tekrar deneyin." },
      { status: 429 }
    );
  }

  let body: { username?: string; password?: string };
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ success: false, message: "Geçersiz istek." }, { status: 400 });
  }

  const { username, password } = body;

  // Boş alan kontrolü
  if (!username || !password) {
    return NextResponse.json({ success: false, message: "Kullanıcı adı ve şifre zorunludur." }, { status: 400 });
  }

  const hashedUsername = crypto.createHash("sha256").update(username).digest("hex");
  const hashedPassword = crypto.createHash("sha256").update(password).digest("hex");

  // Timing-safe karşılaştırma (timing attack koruması)
  const usernameMatch = crypto.timingSafeEqual(
    Buffer.from(hashedUsername.padEnd(64)),
    Buffer.from(ADMIN_USERNAME_HASH.padEnd(64))
  );
  const passwordMatch = crypto.timingSafeEqual(
    Buffer.from(hashedPassword.padEnd(64)),
    Buffer.from(ADMIN_PASSWORD_HASH.padEnd(64))
  );

  if (usernameMatch && passwordMatch) {
    clearFailures(ip);

    // Rastgele güvenli session token üret
    const sessionToken = crypto.randomBytes(32).toString("hex");

    const response = NextResponse.json({ success: true });
    response.cookies.set("admin_session", sessionToken, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "strict",
      maxAge: 60 * 60 * 8, // 8 saat
      path: "/",
    });
    // Token'ı sunucu tarafında da saklayalım (process memory — basit yöntem)
    (global as any).__adminToken = sessionToken;
    return response;
  }

  recordFailure(ip);
  const record = failedAttempts.get(ip);
  const remaining = MAX_ATTEMPTS - (record?.count ?? 0);

  return NextResponse.json(
    {
      success: false,
      message: remaining > 0
        ? `Geçersiz kullanıcı adı veya şifre. ${remaining} deneme hakkınız kaldı.`
        : "Hesap kilitlendi. 15 dakika sonra tekrar deneyin.",
    },
    { status: 401 }
  );
}
