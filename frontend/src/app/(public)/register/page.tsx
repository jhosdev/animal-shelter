'use client';

import { useState } from 'react';
import { TextInput, PasswordInput, Button, Group, Paper, Title, Text, Container, Anchor, Select } from '@mantine/core';
import { useForm } from '@mantine/form';
import api from '@/utils/api';
import { useRouter } from 'next/navigation';
import { setAuthTokens } from '@/utils/auth';
import { userAtom } from '@/atoms/userAtom';
import { useAtom } from 'jotai';

export default function Register() {
  const [error, setError] = useState('');
  const [, setUser] = useAtom(userAtom);
  const router = useRouter();

  const form = useForm({
    initialValues: {
      username: '',
      email: '',
      password: '',
      first_name: '',
      last_name: '',
      role: 'ADOPTER',
    },
  });

  const handleSubmit = async (values: typeof form.values) => {
    try {
      // Register the user
      await api.post('/users/', values);

      // Log in the user
      const loginResponse = await api.post('/token/', {
        username: values.username,
        password: values.password,
      });

      if (loginResponse.status === 200) {
        await setAuthTokens(loginResponse.data.access, loginResponse.data.refresh);
        const { data } = await api.get('/users/me/');
        setUser(data);
        router.push('/animals');
      } else {
        setError('Registration successful but login failed. Please try again.');
      }
    } catch (err) {
      setError('Registration failed. Please try again.');
    }
  };

  return (
    <Container size={420} my={40} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
      <Title ta="center" mb="md">Create an Account</Title>
      <Paper withBorder shadow="md" py={40} px={30} m={10} w={400} radius="md">
        <form onSubmit={form.onSubmit(handleSubmit)}>
          <TextInput
            label="Username"
            placeholder="Your username"
            required
            {...form.getInputProps('username')}
            mb="md"
          />
          <TextInput
            label="Email"
            placeholder="Your email"
            type="email"
            required
            {...form.getInputProps('email')}
            mb="md"
          />
          <PasswordInput
            label="Password"
            placeholder="Your password"
            required
            {...form.getInputProps('password')}
            mb="md"
          />
          <TextInput
            label="First Name"
            placeholder="Your first name"
            {...form.getInputProps('first_name')}
            mb="md"
          />
          <TextInput
            label="Last Name"
            placeholder="Your last name"
            {...form.getInputProps('last_name')}
            mb="md"
          />
          <Select
            label="Role"
            placeholder="Select a role"
            data={[
              { value: 'ADOPTER', label: 'Adopter' },
              { value: 'VOLUNTEER', label: 'Volunteer' },
            ]}
            {...form.getInputProps('role')}
            mb="md"
          />
          <Group justify="center" mt="md">
            <Button type="submit">Register</Button>
          </Group>
        </form>
        {error && <Text c="red" mt="md">{error}</Text>}
        <Group justify="center" mt="md">
          <Anchor component="button" onClick={() => router.push('/')} size="sm">
            Go To Home
          </Anchor>
        </Group>
      </Paper>
    </Container>
  );
}
