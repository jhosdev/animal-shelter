import Image from 'next/image';
import { Button, Group, Text, Container, Paper } from '@mantine/core';
import Link from 'next/link';

export default function Home() {
  return (
    <Container size="xs" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '100vh' }}>
      <Paper p="md" shadow="xs" radius="md" style={{ textAlign: 'center', width: '100%' }}>
        <Text size="xl" mb="md" ta='center'>
          Welcome to Animal Shelter
        </Text>
        <Text size="md" c="dimmed" mb="lg">
          Our mission is to provide a safe and loving environment for animals in need. Explore our platform to adopt a new furry friend or contribute to our cause.
        </Text>
        <Group dir="column" grow>
          <Link href="/login" passHref>
            <Button size="lg" fullWidth>
              Login
            </Button>
          </Link>
          <Link href="/register" passHref>
            <Button size="lg" fullWidth>
              Register
            </Button>
          </Link>
        </Group>
      </Paper>
    </Container>
  );
}
