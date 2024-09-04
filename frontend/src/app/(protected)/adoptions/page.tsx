'use client'
import { useState, useEffect } from 'react';
import { Button, Text, Group, Title } from '@mantine/core';
import api from '@/utils/api';
import DataTable from '@/components/DataTable';
import GenericModal from '@/components/GenericModal';

import { useAtom } from 'jotai';
import { userAtom } from '@/atoms/userAtom';
import { notifications } from '@mantine/notifications';

interface Adoption { 
  id: number; 
  date: string;
  status: 'PENDING' | 'COMPLETED' | 'CANCELLED'; 
  animal: number;
  adopter: number;
  volunteer: number;
}

export default function Adoptions() {
  const [user,] = useAtom(userAtom);
  const [adoptions, setAdoptions] = useState<Adoption[]>([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedAdoption, setSelectedAdoption] = useState<Adoption | null>(null);

  useEffect(() => { fetchAdoptions(); }, []);

  const fetchAdoptions = async () => {
    try {
      const { data } = await api.get('/adoptions/');
      setAdoptions(data);
    } catch (err) {
      showErrorNotification('Failed to fetch adoptions', err);
    }
  };

  const handleSave = async (adoption: Adoption) => {
    try {
      const changedFields = Object.keys(adoption).reduce((acc, key) => {
        const _key = key as keyof Adoption;
        if (selectedAdoption && adoption[key as keyof Adoption] !== selectedAdoption[key as keyof Adoption]) {
          acc[_key] = adoption[_key] as any; 
        }
        return acc;
      }, {} as Partial<Adoption>);

      if (selectedAdoption) {
        await api.patch(`/adoptions/${selectedAdoption.id}/`, changedFields);
      } else {
        await api.post('/adoptions/', adoption);
      }
      fetchAdoptions();
    } catch (err) {
      showErrorNotification('Failed to save adoption', err);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await api.delete(`/adoptions/${id}/`);
      fetchAdoptions();
    } catch (err) {
      showErrorNotification('Failed to delete adoption', err);
    }
  };

  const showErrorNotification = (message: string, err: unknown) => {
    console.error('err:',err);
    notifications.show({
      title: 'Error',
      message,
      color: 'red',
      position: 'top-right',
    });
  };

  const adoptionFields = {
    id: { label: 'ID', type: 'number' as const, editable: false },
    animal: { label: 'Animal ID', type: 'number' as const, editable: true },
    adopter: { label: 'Adopter ID', type: 'number' as const, editable: true },
    status: { 
      label: 'Status', 
      type: 'select' as const, 
      editable: true, 
      options: [
        { value: 'PENDING', label: 'Pending' },
        { value: 'COMPLETED', label: 'Completed' },
        { value: 'CANCELLED', label: 'Cancelled' }
      ],
    },
    date: { label: 'Date', type: 'date' as const, editable: false },
    volunteer: { label: 'Volunteer ID', type: 'number' as const, editable: false},
  };

  const adoptionActions = (adoption: Adoption) => {
    const actions = [] as JSX.Element[];
    if (user?.role === 'ADOPTER') return actions;
    actions.push(
      <Button key="edit" onClick={() => { setSelectedAdoption(adoption); setModalOpen(true); }}>Edit</Button>
    )
    if (user?.role === 'ADMIN') {
      actions.push(
        <Button key="delete" onClick={() => handleDelete(adoption.id)}>Delete</Button>
      );
    }
    return actions;
  };

  return (
    <>
      <Title order={1} mb="lg">Adoptions</Title>
      <DataTable
      data={adoptions}
      columns={['ID', 'Date', 'Status', 'Animal ID', 'Adopter ID', 'Volunteer ID']}
      actions={adoptionActions}
      typeLabels={{
        status: {
          PENDING: 'Pending',
          COMPLETED: 'Completed',
          CANCELLED: 'Cancelled',
        },
      }}
      />
      <GenericModal
        opened={modalOpen}
        onClose={() => setModalOpen(false)}
        onSubmit={handleSave}
        fields={adoptionFields}
        initialValues={selectedAdoption || {} as Adoption}
      />
    </>
  );
}
