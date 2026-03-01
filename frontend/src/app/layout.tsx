import Link from "next/link";
import "./globals.css";

export default function Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html>
      <body className="p-6 font-sans">
        <nav className="flex gap-6 mb-6 border-b pb-2">
          <Link href="/books">Books</Link>
          <Link href="/members">Members</Link>
          <Link href="/borrowings">Borrowings</Link>
        </nav>
        {children}
      </body>
    </html>
  );
}