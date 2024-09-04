'use client';

import { useState } from 'react';
import { TextInput, PasswordInput, Button, Group, Paper, Title, Text, Container, Anchor } from '@mantine/core';
import { useForm } from '@mantine/form';
import { setAuthTokens } from '@/utils/auth';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import api from '@/utils/api';
import { useAtom } from 'jotai';
import { userAtom } from '@/atoms/userAtom';

export default function Login() {
  const [error, setError] = useState('');
  const [, setUser] = useAtom(userAtom);
  const router = useRouter();

  const form = useForm({
    initialValues: {
      username: '',
      password: '',
    },
  });

  const handleSubmit = async (values: typeof form.values) => {
    try {
      const headers = {
        'Content-Type': 'application/json',
      };
      const response = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/token/`, values, { headers });

      if (response.status === 200) {
        await setAuthTokens(response.data.access, response.data.refresh);
        const { data } = await api.get('/users/me/');
        setUser(data);
        router.push('/animals');
      } else {
        setError('Invalid credentials');
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
    }
  };

  return (
    <Container size={420} my={40} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
      <Title ta="center" mb="md">Welcome back!</Title>
      <Text c="dimmed" size="sm" ta="center" m={5}>
          Do not have an account yet?{' '}
          <Anchor component="button" onClick={() => router.push('/register')}>
            Create account
          </Anchor>
        </Text>
      <Paper withBorder shadow="md" py={40} px={30} m={10} w={400} radius="md">
        <form onSubmit={form.onSubmit(handleSubmit)}>
          <TextInput
            label="Username"
            placeholder="Your username"
            required
            {...form.getInputProps('username')}
            mb="md"
          />
          <PasswordInput
            label="Password"
            placeholder="Your password"
            required
            {...form.getInputProps('password')}
            mb="md"
          />
          <Group justify="apart" mt="md">
            <Button type="submit" fullWidth>
              Login
            </Button>
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
