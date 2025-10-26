import type { Metadata } from "next";
import "@/app/globals.css";
import { AuthProvider } from "@/components/auth/AuthProvider";
import NavBar from "@/components/NavBar";

export const metadata: Metadata = {
  title: "Study Spark",
  description: "Focus better with Pomodoro + attention tracking",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <NavBar />
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}