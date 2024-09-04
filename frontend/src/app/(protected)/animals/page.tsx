// pages/animals/index.tsx
'use client'
import { useState, useEffect } from 'react';
import { Button, Text, Group, Title } from '@mantine/core';
import api from '@/utils/api';
import DataTable from '@/components/DataTable';
import GenericModal from '@/components/GenericModal';

import { notifications } from '@mantine/notifications';

import { useAtom } from 'jotai';
import { userAtom } from '@/atoms/userAtom';

interface Animal { id: number; name: string; age: number; breed: string; animal_type: string; status: string; volunteer: number; }

export default function Animals() {
  const [user,] = useAtom(userAtom);
  const [animals, setAnimals] = useState<Animal[]>([]);

  const [modalOpen, setModalOpen] = useState(false);
  const [selectedAnimal, setSelectedAnimal] = useState<Animal | null>(null);

  useEffect(() => { fetchAnimals(); }, []);

  const fetchAnimals = async () => {
    try {
      const { data } = await api.get('/animals/');
      setAnimals(data);
    } catch (err) {
      showErrorNotification('Failed to fetch animals', err);
    }
  };

  const handleAdopt = async (animalId: number) => {
    try {
      await api.post('/adoptions/', { animal: animalId });
      fetchAnimals();
    } catch (err) {
      showErrorNotification('Failed to adopt animal', err);
    }
  };

  const handleSave = async (animal: Animal) => {
    try {
      const changedFields = Object.keys(animal).reduce((acc, key) => {
        const _key = key as keyof Animal;
        if (selectedAnimal && animal[key as keyof Animal] !== selectedAnimal[key as keyof Animal]) {
          acc[_key] = animal[_key] as any; 
        }
        return acc;
      }, {} as Partial<Animal>);

      if (selectedAnimal) {
        await api.patch(`/animals/${selectedAnimal.id}/`, changedFields);
      } else {
        await api.post('/animals/', {
          ...animal,
          status: 'AVAILABLE',
        });
      }
      fetchAnimals();
    } catch (err) {
      showErrorNotification('Failed to save animal', err);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await api.delete(`/animals/${id}/`);
      fetchAnimals();
    } catch (err) {
      showErrorNotification('Failed to delete animal', err);
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

  const animalFields = {
    id: { label: 'ID', type: 'number' as const, editable: false }, // Campo ineditable
    name: { label: 'Name', type: 'text' as const, editable: true },
    age: { label: 'Age', type: 'number' as const, editable: true },
    breed: { label: 'Breed', type: 'text' as const, editable: true },
    animal_type: {
      label: 'Type', type: 'select' as const, editable: true, options: [
        { value: 'DOG', label: 'Dog' },
        { value: 'CAT', label: 'Cat' },
      ]
    },
    status: {
      label: 'Status', type: 'select' as const, editable: true, only_editable:true, options: [
        { value: 'AVAILABLE', label: 'Available' },
        { value: 'ADOPTED', label: 'Adopted' },
        { value: 'PENDING', label: 'Pending adoption' },
      ]
    },
    volunteer: { label: 'Volunteer', type: 'number' as const, editable: false },
  };

  const animalActions = (animal: Animal) => {
    
    if (user?.role === 'ADOPTER') {
      return [
        <Button key="adopt" onClick={() => handleAdopt(animal.id)}>Adopt</Button>,
      ];
    }

    return [
      <Button key="edit" onClick={() => { setSelectedAnimal(animal); setModalOpen(true); }}>Edit</Button>,
        <Button key="delete" onClick={() => handleDelete(animal.id)}>Delete</Button>
    ]
  };

  return (
    <>
      <Title order={1} mb="lg">Animals</Title>
      {user?.role !== 'ADOPTER' && (
        <Group mb="md">
          <Button onClick={() => { setSelectedAnimal(null); setModalOpen(true); }}>Add New Animal</Button>
        </Group>
      )}
      <DataTable
        data={animals}
        columns={['ID', 'Name', 'Age', 'Breed', 'Type', 'Status', 'Volunteer']}
        actions={animalActions}
        typeLabels={{
          animal_type: {
            DOG: 'Dog',
            CAT: 'Cat',
          },
          status: {
            AVAILABLE: 'Available',
            ADOPTED: 'Adopted',
            PENDING: 'Pending adoption',
          },
        }}/>
      <GenericModal
        opened={modalOpen}
        onClose={() => setModalOpen(false)}
        onSubmit={handleSave}
        fields={animalFields}
        initialValues={selectedAnimal || {
          name: '',
          breed: '',
        } as Animal}
      />
    </>
  );
}
