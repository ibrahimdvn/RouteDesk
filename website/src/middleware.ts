import { NextRequest, NextResponse } from "next/server";

export function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl;

  // Admin login sayfası ve API rotalarına izin ver
  if (
    pathname.startsWith("/admin/login") ||
    pathname.startsWith("/api/admin/login") ||
    pathname.startsWith("/api/admin/logout")
  ) {
    return NextResponse.next();
  }

  // Diğer /admin rotalarını koru
  if (pathname.startsWith("/admin")) {
    const token = req.cookies.get("admin_session")?.value;
    const serverToken = (global as any).__adminToken;

    // Token yoksa veya sunucu tokenıyla eşleşmiyorsa giriş sayfasına yönlendir
    const isValid = token && serverToken && token === serverToken;

    if (!isValid) {
      const loginUrl = new URL("/admin/login", req.url);
      return NextResponse.redirect(loginUrl);
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/admin/:path*", "/api/admin/:path*"],
};
