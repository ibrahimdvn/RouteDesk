import { NextRequest, NextResponse } from "next/server";

const ADMIN_USERNAME = "admin_1";
const ADMIN_PASSWORD = "Aslandur1881_";

export async function POST(req: NextRequest) {
  const body = await req.json();
  const { username, password } = body;

  if (username === ADMIN_USERNAME && password === ADMIN_PASSWORD) {
    const response = NextResponse.json({ success: true });
    response.cookies.set("admin_session", "authenticated", {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "strict",
      maxAge: 60 * 60 * 8, // 8 saat
      path: "/",
    });
    return response;
  }

  return NextResponse.json({ success: false, message: "Geçersiz kullanıcı adı veya şifre." }, { status: 401 });
}
