'use client';

import React from 'react';

interface PropertyFormData {
  name: string;
  address: string;
  number_of_units: string;
  number_of_tenants: string;
  status: 'active' | 'archived';
}

interface PropertyFormProps {
  initialData?: Partial<PropertyFormData>;
}

export default function PropertyForm({ initialData }: PropertyFormProps) {
  return (
    <div className="space-y-6">
      <div>
        <label
          htmlFor="name"
          className="block text-sm font-semibold text-gray-700 mb-2"
        >
          Apartment Name <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          id="name"
          name="name"
          defaultValue={initialData?.name || ''}
          required
          className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#FFA719] focus:border-[#FFA719] outline-none transition-colors bg-[#FFFADA] text-[#2a2a2a]"
          placeholder="Enter apartment name"
        />
      </div>

      <div>
        <label
          htmlFor="address"
          className="block text-sm font-semibold text-gray-700 mb-2"
        >
          Address <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          id="address"
          name="address"
          defaultValue={initialData?.address || ''}
          required
          className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#FFA719] focus:border-[#FFA719] outline-none transition-colors bg-[#FFFADA] text-[#2a2a2a]"
          placeholder="Enter full address"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label
            htmlFor="number_of_units"
            className="block text-sm font-semibold text-gray-700 mb-2"
          >
            Number of Units <span className="text-red-500">*</span>
          </label>
          <input
            type="number"
            id="number_of_units"
            name="number_of_units"
            defaultValue={initialData?.number_of_units || ''}
            required
            min="1"
            className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#FFA719] focus:border-[#FFA719] outline-none transition-colors bg-[#FFFADA] text-[#2a2a2a]"
            placeholder="0"
          />
        </div>

        <div>
          <label
            htmlFor="number_of_tenants"
            className="block text-sm font-semibold text-gray-700 mb-2"
          >
            Number of Tenants <span className="text-red-500">*</span>
          </label>
          <input
            type="number"
            id="number_of_tenants"
            name="number_of_tenants"
            defaultValue={initialData?.number_of_tenants || ''}
            required
            min="0"
            className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#FFA719] focus:border-[#FFA719] outline-none transition-colors bg-[#FFFADA] text-[#2a2a2a]"
            placeholder="0"
          />
        </div>
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
  );
}

