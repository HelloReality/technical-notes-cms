import { NextResponse } from "next/server";
import { destroySession } from "@/lib/auth";

export const dynamic = "force-dynamic";

export async function POST() {
  try {
    await destroySession();
    return NextResponse.json({ success: true });
  } catch (err) {
    const message =
      err instanceof Error ? err.message : "Failed to log out.";
    return NextResponse.json({ success: false, error: message }, { status: 500 });
  }
}
