'use client'
import { useState, useEffect } from 'react';
import { Button, Text, Group, Title } from '@mantine/core';
import api from '@/utils/api';
import DataTable from '@/components/DataTable';
import GenericModal from '@/components/GenericModal';

import { useAtom } from 'jotai';
import { userAtom } from '@/atoms/userAtom';
import { notifications } from '@mantine/notifications';

interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role: 'ADMIN' | 'VOLUNTEER' | 'ADOPTER';
  status: 'ACTIVE' | 'INACTIVE';
}

export default function Users() {
  const [user,] = useAtom(userAtom);
  const [users, setUsers] = useState<User[]>([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);

  useEffect(() => { fetchUsers(); }, []);

  const fetchUsers = async () => {
    try {
      const { data } = await api.get('/users/');
      setUsers(data);
    } catch (err) {
      showErrorNotification('Failed to fetch users', err);
    }
  };

  const handleSave = async (user: User) => {
    try {
      const changedFields = Object.keys(user).reduce((acc, key) => {
        const _key = key as keyof User;
        if (selectedUser && user[key as keyof User] !== selectedUser[key as keyof User]) {
          acc[_key] = user[_key] as any; 
        }
        return acc;
      }, {} as Partial<User>);

      if (selectedUser) {
        await api.patch(`/users/${selectedUser.id}/`, changedFields);
      } else {
        await api.post('/users/', user);
      }
      fetchUsers();
    } catch (err) {
      showErrorNotification('Failed to save user', err);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await api.delete(`/users/${id}/`);
      fetchUsers();
    } catch (err) {
      showErrorNotification('Failed to delete user', err);
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

  const userFields = {
    id: { label: 'ID', type: 'number' as const, editable: false },
    username: { label: 'Username', type: 'text' as const, editable: true },
    email: { label: 'Email', type: 'text' as const, editable: true },
    first_name: { label: 'First Name', type: 'text' as const, editable: true },
    last_name: { label: 'Last Name', type: 'text' as const, editable: true },
    role: {
      label: 'Role',
      type: 'select' as const,
      editable: true,
      options: [
        { value: 'VOLUNTEER', label: 'Volunteer' },
        { value: 'ADOPTER', label: 'Adopter' }
      ]
    },
    status: {
      label: 'Status',
      type: 'select' as const,
      editable: true,
      options: [
        { value: 'ACTIVE', label: 'Active' },
        { value: 'INACTIVE', label: 'Inactive' }
      ]
    }
  };

  const userActions = (_user: User) => {
    const actions = [] as JSX.Element[];
    if (user?.role == 'VOLUNTEER') {
      return actions
    }
    actions.push(
      <Button key="edit" onClick={() => { setSelectedUser(_user); setModalOpen(true); }}>Edit</Button>,
      <Button key="delete" onClick={() => handleDelete(_user.id)}>Delete</Button>
    );
    return actions;
  };

  return (
    <>
      <Title order={1} mb="lg">Users</Title>
      {user?.role === 'ADOPTER' && (
        <Group mb="md">
          <Button onClick={() => { setSelectedUser(null); setModalOpen(true); }}>Add New User</Button>
        </Group>
      )}
      <DataTable
      data={users}
      columns={['ID', 'Username', 'Email', 'First Name', 'Last Name', 'Role', 'Status']}
      actions={userActions}
      typeLabels={{
        role: {
          VOLUNTEER: 'Dog',
          ADMIN: 'Cat',
          ADOPTER: 'Adopter',
        },
        status: {
          ACTIVE: 'Active',
          INACTIVE: 'Inactive',
        },
      }}
      />
      <GenericModal
        opened={modalOpen}
        onClose={() => setModalOpen(false)}
        onSubmit={handleSave}
        fields={userFields}
        initialValues={selectedUser || {} as User}
      />
    </>
  );
}
