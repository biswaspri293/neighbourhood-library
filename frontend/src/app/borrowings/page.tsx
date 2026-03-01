"use client";

import { useEffect, useState } from "react";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000/api";

export default function BorrowingsPage() {
  const [borrowings, setBorrowings] = useState<any[]>([]);
  const [members, setMembers] = useState<any[]>([]);
  const [books, setBooks] = useState<any[]>([]);
  const [statusFilter, setStatusFilter] = useState("");
  const [memberFilter, setMemberFilter] = useState("");
  const [form, setForm] = useState({
    member_id: "",
    book_id: "",
  });

  // -------------------------------
  // Fetch Borrowings
  // -------------------------------
  async function fetchBorrowings() {
    let endpoint = `${API_BASE}/borrowings`;

    if (memberFilter) {
      endpoint = `${API_BASE}/borrowings/member/${memberFilter}`;

      if (statusFilter) {
        endpoint += `?status=${statusFilter}`;
      }
    }
    // If only status filter
    else if (statusFilter) {
      endpoint += `?status=${statusFilter}`;
    }
    const res = await fetch(endpoint, { cache: "no-store" });
    const data = await res.json();
    setBorrowings(data);
  }

  // -------------------------------
  // Fetch Members & Books
  // -------------------------------
  async function fetchMembers() {
    const res = await fetch(`${API_BASE}/members`);
    setMembers(await res.json());
  }

  async function fetchBooks() {
    const res = await fetch(`${API_BASE}/books`);
    setBooks(await res.json());
  }

  // Re-run when filter changes
  useEffect(() => {
  fetchBorrowings();
  }, [statusFilter, memberFilter]);

  // Load members & books once
  useEffect(() => {
    fetchMembers();
    fetchBooks();
  }, []);

  // -------------------------------
  // Borrow Book
  // -------------------------------
  async function handleBorrow() {
    if (!form.member_id || !form.book_id) {
      alert("Select member and book");
      return;
    }

    const res = await fetch(`${API_BASE}/borrowings`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        member_id: Number(form.member_id),
        book_id: Number(form.book_id),
      }),
    });

    if (!res.ok) {
      alert((await res.json()).detail);
      return;
    }

    setForm({ member_id: "", book_id: "" });
    fetchBorrowings();
    fetchBooks();
  }

  // -------------------------------
  // Return Book
  // -------------------------------
  async function handleReturn(id: number) {
    const res = await fetch(
      `${API_BASE}/borrowings/${id}/return`,
      {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: "RETURNED" }),
      }
    );

    if (!res.ok) {
      alert((await res.json()).detail);
      return;
    }

    fetchBorrowings();
    fetchBooks();
  }

  return (
    <div>
      <h1 className="text-xl mb-4">Borrowings</h1>

      {/* Borrow Form */}
      <div className="mb-4 space-x-2">
        <select
          className="border p-2"
          value={form.member_id}
          onChange={(e) =>
            setForm({ ...form, member_id: e.target.value })
          }
        >
          <option value="">Select Member</option>
          {members.map((m) => (
            <option key={m.id} value={m.id}>
              {m.name}
            </option>
          ))}
        </select>

        <select
          className="border p-2"
          value={form.book_id}
          onChange={(e) =>
            setForm({ ...form, book_id: e.target.value })
          }
        >
          <option value="">Select Book</option>
          {books
            .filter((b) => b.available_copies > 0)
            .map((b) => (
              <option key={b.id} value={b.id}>
                {b.title} ({b.available_copies} available)
              </option>
            ))}
        </select>

        <button
          onClick={handleBorrow}
          className="bg-blue-500 text-white px-4 py-2"
        >
          Borrow
        </button>
      </div>

      {/* Filter */}
      <select
        className="border p-2 mb-4"
        value={statusFilter}
        onChange={(e) => setStatusFilter(e.target.value)}
      >
        <option value="">All</option>
        <option value="BORROWED">Borrowed</option>
        <option value="RETURNED">Returned</option>
      </select>

      <select
        className="border p-2 mb-4 ml-4"
        value={memberFilter}
        onChange={(e) => setMemberFilter(e.target.value)}
      >
        <option value="">All Members</option>
        {members.map((m) => (
        <option key={m.id} value={m.id}>
        {m.name}
        </option>
        ))}
      </select>

      {/* Table */}
      <table className="w-full border border-gray-600 border-collapse text-left">
  <thead className="bg-gray-800 text-gray-200">
    <tr>
      <th className="border border-gray-600 p-2">ID</th>
      <th className="border border-gray-600 p-2">Book</th>
      <th className="border border-gray-600 p-2">Member</th>
      <th className="border border-gray-600 p-2">Borrowed At</th>
      <th className="border border-gray-600 p-2">Due Date</th>
      <th className="border border-gray-600 p-2">Returned At</th>
      <th className="border border-gray-600 p-2">Status</th>
      <th className="border border-gray-600 p-2 text-center">Action</th>
    </tr>
  </thead>

  <tbody>
    {borrowings.map((b) => (
      <tr
        key={b.id}
        className="hover:bg-gray-700 transition-colors"
      >
        <td className="border border-gray-600 p-2">{b.id}</td>

        <td className="border border-gray-600 p-2">
          {b.book_title}
        </td>

        <td className="border border-gray-600 p-2">
          {b.member_name}
        </td>

        <td className="border border-gray-600 p-2">
          {b.borrowed_at
            ? new Date(b.borrowed_at).toLocaleDateString()
            : "-"}
        </td>

        <td className="border border-gray-600 p-2">
          {b.due_date
            ? new Date(b.due_date).toLocaleDateString()
            : "-"}
        </td>

        <td className="border border-gray-600 p-2">
          {b.returned_at
            ? new Date(b.returned_at).toLocaleDateString()
            : "-"}
        </td>

        <td className="border border-gray-600 p-2">
          <span
            className={
              b.status === "BORROWED"
                ? "text-yellow-400 font-medium"
                : "text-green-400 font-medium"
            }
          >
            {b.status}
          </span>
        </td>

        <td className="border border-gray-600 p-2 text-center">
          {b.status === "BORROWED" && (
            <button
              onClick={() => handleReturn(b.id)}
              className="text-green-500 hover:text-green-400"
            >
              Return
            </button>
          )}
        </td>
      </tr>
    ))}
  </tbody>
</table>
    </div>
  );
}