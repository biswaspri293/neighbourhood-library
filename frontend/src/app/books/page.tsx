"use client";

import { useEffect, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000/api";

export default function BooksPage() {
  const [books, setBooks] = useState<any[]>([]);
  const [filter, setFilter] = useState("");
  const [selected, setSelected] = useState<number[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [form, setForm] = useState({
    id: "",
    title: "",
    author: "",
    total_copies: "",
  });

  async function fetchBooks() {
    const res = await fetch(`${API_BASE}/books`, { cache: "no-store" });
    const data = await res.json();
    setBooks(data);
  }

  useEffect(() => {
    fetchBooks();
  }, []);

  async function handleAdd() {
  const res = await fetch(`${API_BASE}/books`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      title: form.title,
      author: form.author,
      total_copies: Number(form.total_copies),
    }),
  });

  if (!res.ok) {
    const data = await res.json();

    if (Array.isArray(data.detail)) {
      setError(data.detail.map((e: any) => e.msg).join(", "));
    } else {
      setError(data.detail || "Something went wrong");
    }

    return;
  }

  resetForm();
  fetchBooks();
}

  async function handleUpdate() {
  if (!form.id) {
    alert("Select a book first");
    return;
  }

  const res = await fetch(`${API_BASE}/books/${form.id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      title: form.title,
      author: form.author,
      total_copies: Number(form.total_copies),
    }),
  });

  if (!res.ok) {
    const data = await res.json();

    if (Array.isArray(data.detail)) {
      setError(data.detail.map((e: any) => e.msg).join(", "));
    } else {
      setError(data.detail || "Update failed");
    }

    return;
  }

  resetForm();
  fetchBooks();
 }

async function handleDelete(id: number) {
  if (!confirm("Delete this book?")) return;

  const res = await fetch(`${API_BASE}/books/${id}`, {
    method: "DELETE",
  });

  if (!res.ok) {
    const data = await res.json();
    setError(data.detail || "Delete failed");
    return;
  }

  fetchBooks();
}

  async function handleBulkDelete() {
    for (const id of selected) {
      await fetch(`${API_BASE}/books/${id}`, {
        method: "DELETE",
      });
    }

    setSelected([]);
    fetchBooks();
  }

  function resetForm() {
    setForm({
      id: "",
      title: "",
      author: "",
      total_copies: "",
    });
  }

  const filteredBooks = books.filter((b) =>
    Object.values(b)
      .join(" ")
      .toLowerCase()
      .includes(filter.toLowerCase())
  );

  return (
    <div>
      <h1 className="text-xl mb-4">Books</h1>
      {error && (
        <div className="bg-red-100 text-red-700 p-2 mb-4 border border-red-400 rounded flex justify-between items-center">
            <span>{error}</span>
            <button
                onClick={() => setError(null)}
                className="ml-4 font-bold text-red-700 hover:text-red-900"
            >
              ✕
            </button>
          </div>
        )}
      {/* FILTER */}
      <input
        placeholder="Filter by id, title, author..."
        className="border p-2 mb-4 w-full"
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
      />

      {/* FORM */}
      <div className="mb-4 space-x-2">
        <input
          placeholder="Title"
          className="border p-2"
          value={form.title}
          onChange={(e) =>
            setForm({ ...form, title: e.target.value })
          }
        />
        <input
          placeholder="Author"
          className="border p-2"
          value={form.author}
          onChange={(e) =>
            setForm({ ...form, author: e.target.value })
          }
        />
        <input
          placeholder="Total Copies"
          className="border p-2"
          value={form.total_copies}
          onChange={(e) =>
            setForm({ ...form, total_copies: e.target.value })
          }
        />

        <button
          onClick={handleAdd}
          className="bg-blue-500 text-white px-4 py-2"
        >
          Add
        </button>

        <button
          onClick={handleUpdate}
          className="bg-yellow-500 text-white px-4 py-2"
        >
          Update
        </button>

{/*         <button
          onClick={handleBulkDelete}
          className="bg-red-500 text-white px-4 py-2"
        >
          Delete Selected
        </button> */}
      </div>

      {/* TABLE */}
      <table className="w-full border border-gray-600 border-collapse text-left">
  <thead className="bg-gray-800 text-gray-200">
          <tr>
            <th className="border p-2"></th>
            <th className="border p-2">ID</th>
            <th className="border p-2">Title</th>
            <th className="border p-2">Author</th>
            <th className="border p-2">Total</th>
            <th className="border p-2">Available</th>
            <th className="border p-2">Action</th>
          </tr>
        </thead>
        <tbody>
          {filteredBooks.map((b) => (
            <tr
  key={b.id}
  onClick={() =>
    setForm({
      id: b.id.toString(),
      title: b.title,
      author: b.author,
      total_copies: b.total_copies.toString(),
    })
  }
  className="cursor-pointer hover:bg-gray-700 transition-colors"
>
              <td className="border p-2">
                <input
                  type="checkbox"
                  checked={selected.includes(b.id)}
                  onChange={(e) => {
                    if (e.target.checked) {
                      setSelected([...selected, b.id]);
                    } else {
                      setSelected(
                        selected.filter((x) => x !== b.id)
                      );
                    }
                  }}
                />
              </td>
              <td className="border p-2">{b.id}</td>
              <td className="border p-2">{b.title}</td>
              <td className="border p-2">{b.author}</td>
              <td className="border p-2">{b.total_copies}</td>
              <td className="border p-2">
                {b.available_copies}
              </td>
              <td className="border p-2">
                <button
                  onClick={() => handleDelete(b.id)}
                  className="text-red-600"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}