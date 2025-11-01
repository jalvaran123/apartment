'use client';

import React, { useEffect, useState } from 'react';

interface Unit {
  id: number;
  name: string;
  apartment: string;
}

interface TenantFormData {
  first_name: string;
  middle_name: string;
  last_name: string;
  sex: 'M' | 'F';
  date_of_birth: string;
  contact_number: string;
  original_address: string;
  unit: string;
  move_in_date: string;
  move_out_date?: string;
  status: 'active' | 'archived';
}

interface TenantFormProps {
  initialData?: Partial<TenantFormData>;
  units?: Unit[];
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

export default function TenantForm({ initialData, units: propUnits }: TenantFormProps) {
  const [units, setUnits] = useState<Unit[]>(propUnits || []);

  useEffect(() => {
    // Fetch units if not provided
    if (!propUnits || propUnits.length === 0) {
      fetch(`${API_BASE_URL}/api/units/`)
        .then((res) => res.json())
        .then((data) => setUnits(data))
        .catch((err) => console.error('Error fetching units:', err));
    }
  }, [propUnits]);

  return (
    <div className="space-y-6">
      {/* Personal Information */}
      <div className="space-y-4 border-b border-gray-200 pb-6">
        <h3 className="text-sm font-semibold text-gray-600 uppercase tracking-wide">
          Personal Information
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label
              htmlFor="first_name"
              className="block text-sm font-semibold text-gray-700 mb-2"
            >
              First Name <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              id="first_name"
              name="first_name"
              defaultValue={initialData?.first_name || ''}
              required
              className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#FFA719] focus:border-[#FFA719] outline-none transition-colors bg-[#FFFADA] text-[#2a2a2a]"
            />
          </div>

          <div>
            <label
              htmlFor="middle_name"
              className="block text-sm font-semibold text-gray-700 mb-2"
            >
              Middle Name
            </label>
            <input
              type="text"
              id="middle_name"
              name="middle_name"
              defaultValue={initialData?.middle_name || ''}
              className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#FFA719] focus:border-[#FFA719] outline-none transition-colors bg-[#FFFADA] text-[#2a2a2a]"
            />
          </div>

          <div>
            <label
              htmlFor="last_name"
              className="block text-sm font-semibold text-gray-700 mb-2"
            >
              Last Name <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              id="last_name"
              name="last_name"
              defaultValue={initialData?.last_name || ''}
              required
              className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#FFA719] focus:border-[#FFA719] outline-none transition-colors bg-[#FFFADA] text-[#2a2a2a]"
            />
          </div>

          <div>
            <label
              htmlFor="sex"
              className="block text-sm font-semibold text-gray-700 mb-2"
            >
              Sex <span className="text-red-500">*</span>
            </label>
            <select
              id="sex"
              name="sex"
              defaultValue={initialData?.sex || 'M'}
              required
              className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#FFA719] focus:border-[#FFA719] outline-none transition-colors bg-[#FFFADA] text-[#2a2a2a]"
            >
              <option value="M">Male</option>
              <option value="F">Female</option>
            </select>
          </div>

          <div>
            <label
              htmlFor="date_of_birth"
              className="block text-sm font-semibold text-gray-700 mb-2"
            >
              Date of Birth <span className="text-red-500">*</span>
            </label>
            <input
              type="date"
              id="date_of_birth"
              name="date_of_birth"
              defaultValue={initialData?.date_of_birth || ''}
              required
              className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#FFA719] focus:border-[#FFA719] outline-none transition-colors bg-[#FFFADA] text-[#2a2a2a]"
            />
          </div>

          <div>
            <label
              htmlFor="contact_number"
              className="block text-sm font-semibold text-gray-700 mb-2"
            >
              Contact Number <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              id="contact_number"
              name="contact_number"
              defaultValue={initialData?.contact_number || ''}
              required
              className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#FFA719] focus:border-[#FFA719] outline-none transition-colors bg-[#FFFADA] text-[#2a2a2a]"
            />
          </div>
        </div>

        <div>
          <label
            htmlFor="original_address"
            className="block text-sm font-semibold text-gray-700 mb-2"
          >
            Original Address
          </label>
          <textarea
            id="original_address"
            name="original_address"
            rows={3}
            defaultValue={initialData?.original_address || ''}
            className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#FFA719] focus:border-[#FFA719] outline-none transition-colors bg-[#FFFADA] text-[#2a2a2a] resize-none"
          />
        </div>
      </div>

      {/* Unit Assignment */}
      <div className="space-y-4">
        <h3 className="text-sm font-semibold text-gray-600 uppercase tracking-wide">
          Unit Assignment
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label
              htmlFor="unit"
              className="block text-sm font-semibold text-gray-700 mb-2"
            >
              Unit <span className="text-red-500">*</span>
            </label>
            <select
              id="unit"
              name="unit"
              defaultValue={initialData?.unit || ''}
              required
              className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#FFA719] focus:border-[#FFA719] outline-none transition-colors bg-[#FFFADA] text-[#2a2a2a]"
            >
              <option value="">Select Unit</option>
              {units.map((unit) => (
                <option key={unit.id} value={unit.id}>
                  {unit.name} - {unit.apartment}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label
              htmlFor="move_in_date"
              className="block text-sm font-semibold text-gray-700 mb-2"
            >
              Move-In Date <span className="text-red-500">*</span>
            </label>
            <input
              type="date"
              id="move_in_date"
              name="move_in_date"
              defaultValue={initialData?.move_in_date || ''}
              required
              className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#FFA719] focus:border-[#FFA719] outline-none transition-colors bg-[#FFFADA] text-[#2a2a2a]"
            />
          </div>

          <div>
            <label
              htmlFor="move_out_date"
              className="block text-sm font-semibold text-gray-700 mb-2"
            >
              Move-Out Date
            </label>
            <input
              type="date"
              id="move_out_date"
              name="move_out_date"
              defaultValue={initialData?.move_out_date || ''}
              className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#FFA719] focus:border-[#FFA719] outline-none transition-colors bg-[#FFFADA] text-[#2a2a2a]"
            />
          </div>

          <div>
            <label
              htmlFor="status"
              className="block text-sm font-semibold text-gray-700 mb-2"
            >
              Status <span className="text-red-500">*</span>
            </label>
            <select
              id="status"
              name="status"
              defaultValue={initialData?.status || 'active'}
              required
              className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#FFA719] focus:border-[#FFA719] outline-none transition-colors bg-[#FFFADA] text-[#2a2a2a]"
            >
              <option value="active">Active</option>
              <option value="archived">Archived</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  );
}

