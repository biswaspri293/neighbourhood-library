"use client";

import { useEffect, useState } from "react";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000/api";

export default function MembersPage() {
  const [members, setMembers] = useState<any[]>([]);
  const [selected, setSelected] = useState<number[]>([]);
  const [filter, setFilter] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [form, setForm] = useState({
    id: "",
    name: "",
    email: "",
    phone: "",
  });

  async function fetchMembers() {
    const res = await fetch(`${API_BASE}/members`, {
      cache: "no-store",
    });
    const data = await res.json();
    setMembers(data);
  }

  useEffect(() => {
    fetchMembers();
  }, []);

  async function handleAdd() {
    const res = await fetch(`${API_BASE}/members`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: form.name,
        email: form.email,
        phone: form.phone,
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
    fetchMembers();
  }

  async function handleUpdate() {
    if (!form.id) {
      alert("Select a member first");
      return;
    }

    const res = await fetch(`${API_BASE}/members/${form.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: form.name,
        email: form.email,
        phone: form.phone,
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
    fetchMembers();
  }

  async function handleDelete(id: number) {
    if (!confirm("Delete this member?")) return;

    const res = await fetch(`${API_BASE}/members/${id}`, {
      method: "DELETE",
    });

    if (!res.ok) {
    const data = await res.json();
    setError(data.detail || "Delete failed");
    return;
  }

    fetchMembers();
  }

  async function handleBulkDelete() {
    for (const id of selected) {
      await fetch(`${API_BASE}/members/${id}`, {
        method: "DELETE",
      });
    }

    setSelected([]);
    fetchMembers();
  }

  function resetForm() {
    setForm({
      id: "",
      name: "",
      email: "",
      phone: "",
    });
  }

  const filtered = members.filter((m) =>
    Object.values(m)
      .join(" ")
      .toLowerCase()
      .includes(filter.toLowerCase())
  );

  return (
    <div>
      <h1 className="text-xl mb-4">Members</h1>
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
        placeholder="Filter by id, name, email..."
        className="border p-2 mb-4 w-full"
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
      />

      {/* FORM */}
      <div className="mb-4 space-x-2">
        <input
          placeholder="Name"
          className="border p-2"
          value={form.name}
          onChange={(e) =>
            setForm({ ...form, name: e.target.value })
          }
        />
        <input
          placeholder="Email"
          className="border p-2"
          value={form.email}
          onChange={(e) =>
            setForm({ ...form, email: e.target.value })
          }
        />
        <input
          placeholder="Phone"
          className="border p-2"
          value={form.phone}
          onChange={(e) =>
            setForm({ ...form, phone: e.target.value })
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
      <th className="border border-gray-600 p-2 w-10"></th>
      <th className="border border-gray-600 p-2">ID</th>
      <th className="border border-gray-600 p-2">Name</th>
      <th className="border border-gray-600 p-2">Email</th>
      <th className="border border-gray-600 p-2">Phone</th>
      <th className="border border-gray-600 p-2 text-center">Action</th>
    </tr>
  </thead>

<tbody>
  {filtered.map((m) => (
    <tr
      key={m.id}
      onClick={() =>
        setForm({
          id: m.id.toString(),
          name: m.name,
          email: m.email,
          phone: m.phone || "",
        })
      }
      className="cursor-pointer hover:bg-gray-700 transition-colors"
    >
      <td className="border border-gray-600 p-2 text-center">
        <input
          type="checkbox"
          checked={selected.includes(m.id)}
          onChange={(e) => {
            if (e.target.checked) {
              setSelected((prev) => [...prev, m.id]);
            } else {
              setSelected((prev) =>
                prev.filter((x) => x !== m.id)
              );
            }
          }}
          //onClick={(e) => e.stopPropagation()} // ✅ prevents row click
        />
      </td>

      <td className="border border-gray-600 p-2">{m.id}</td>
      <td className="border border-gray-600 p-2">{m.name}</td>
      <td className="border border-gray-600 p-2">{m.email}</td>
      <td className="border border-gray-600 p-2">{m.phone || "-"}</td>

      <td className="border border-gray-600 p-2 text-center">
        <button
          onClick={() => {
            //e.stopPropagation(); // ✅ prevent row click
            handleDelete(m.id);
          }}
          className="text-red-500 hover:text-red-400"
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