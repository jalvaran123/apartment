'use client';

import React, { useState, useEffect } from 'react';
import SideFormDrawer from '@/components/ui/SideFormDrawer';
import PropertyForm from '@/components/forms/PropertyForm';

interface Apartment {
  id: number;
  name: string;
  address: string;
  number_of_units: number;
  number_of_tenants: number;
  status: 'active' | 'archived';
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

export default function PropertiesPage() {
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [apartments, setApartments] = useState<Apartment[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Fetch apartments
  const fetchApartments = async () => {
    try {
      setIsLoading(true);
      const response = await fetch(`${API_BASE_URL}/api/apartments/`);
      if (response.ok) {
        const data = await response.json();
        setApartments(data);
      }
    } catch (error) {
      console.error('Error fetching apartments:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchApartments();
  }, []);

  // Handle form submission
  const handleAddProperty = async (data: any) => {
    try {
      // Get CSRF token from cookies (Django requirement)
      const csrfToken = document.cookie
        .split('; ')
        .find((row) => row.startsWith('csrftoken='))
        ?.split('=')[1];

      const response = await fetch(`${API_BASE_URL}/accounts/apartments/create/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken || '',
        },
        credentials: 'include',
        body: JSON.stringify({
          name: data.name,
          address: data.address,
          number_of_units: parseInt(data.number_of_units),
          number_of_tenants: parseInt(data.number_of_tenants),
          status: data.status,
        }),
      });

      if (response.ok) {
        // Close drawer and refresh list
        setIsDrawerOpen(false);
        await fetchApartments();
      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.error || 'Failed to create apartment'}`);
      }
    } catch (error) {
      console.error('Error creating apartment:', error);
      alert('Failed to create apartment. Please try again.');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#9D6DC2] to-[#5A2D82] p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-[#6D3A8E] rounded-2xl shadow-lg p-8 mb-6 border border-white/10">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold text-[#FFFADA] mb-2">
                Properties
              </h1>
              <p className="text-[#FFCD7B] text-sm">
                Manage all apartment properties
              </p>
            </div>
            <button
              onClick={() => setIsDrawerOpen(true)}
              className="px-6 py-3 rounded-lg font-semibold text-[#2a2a2a] bg-gradient-to-r from-[#FFA719] to-[#FFCD7B] hover:shadow-lg transition-all transform hover:scale-105"
            >
              ➕ Add Apartment
            </button>
          </div>
        </div>

        {/* Properties Table */}
        <div className="bg-[#6D3A8E] rounded-2xl shadow-lg overflow-hidden border border-white/10">
          {isLoading ? (
            <div className="p-8 text-center text-white">Loading...</div>
          ) : apartments.length === 0 ? (
            <div className="p-8 text-center text-gray-300">
              No apartments available. Click "Add Apartment" to get started.
            </div>
          ) : (
            <table className="w-full">
              <thead>
                <tr className="bg-gradient-to-r from-[#FFA719] to-[#FFCD7B]">
                  <th className="px-6 py-4 text-left font-bold text-[#2a2a2a]">
                    Name
                  </th>
                  <th className="px-6 py-4 text-left font-bold text-[#2a2a2a]">
                    Address
                  </th>
                  <th className="px-6 py-4 text-left font-bold text-[#2a2a2a]">
                    Units
                  </th>
                  <th className="px-6 py-4 text-left font-bold text-[#2a2a2a]">
                    Tenants
                  </th>
                  <th className="px-6 py-4 text-left font-bold text-[#2a2a2a]">
                    Status
                  </th>
                  <th className="px-6 py-4 text-left font-bold text-[#2a2a2a]">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody>
                {apartments.map((apt) => (
                  <tr
                    key={apt.id}
                    className="border-b border-white/10 hover:bg-white/5 transition-colors"
                  >
                    <td className="px-6 py-4 text-white font-semibold">
                      {apt.name}
                    </td>
                    <td className="px-6 py-4 text-gray-200">{apt.address}</td>
                    <td className="px-6 py-4 text-gray-200">
                      {apt.number_of_units}
                    </td>
                    <td className="px-6 py-4 text-gray-200">
                      {apt.number_of_tenants}
                    </td>
                    <td className="px-6 py-4">
                      <span
                        className={`px-3 py-1 rounded-full text-sm font-semibold ${
                          apt.status === 'active'
                            ? 'bg-[#FFA719] text-[#2a2a2a]'
                            : 'bg-[#9D6DC2] text-[#FFFADA]'
                        }`}
                      >
                        {apt.status === 'active' ? 'Active' : 'Archived'}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <button className="text-blue-400 hover:text-blue-300 mr-3">
                        Edit
                      </button>
                      <button className="text-red-400 hover:text-red-300">
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        {/* Side Drawer */}
        <SideFormDrawer
          isOpen={isDrawerOpen}
          title="Add New Property"
          onClose={() => setIsDrawerOpen(false)}
          onSubmit={handleAddProperty}
        >
          <PropertyForm />
        </SideFormDrawer>
      </div>
    </div>
  );
}

