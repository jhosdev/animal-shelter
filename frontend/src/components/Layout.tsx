'use client';
import { AppShell, Burger, Group, NavLink, Button, Text } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAtom } from 'jotai';
import { userAtom } from '@/atoms/userAtom';
import { setAuthTokens } from '@/utils/auth';

export function Shell({ children }: { children: React.ReactNode }) {
  const [opened, { toggle }] = useDisclosure();
  const [user, setUser] = useAtom(userAtom);
  const router = useRouter();

  const handleLogout = async () => {
    setAuthTokens(null, null);
    setUser(null);
    router.push('/');
  };

  const getLinks = () => {
    const commonLinks = [
      { href: '/animals', label: 'Animals' },
    ];

    if (!user) return commonLinks;

    if (user.role === 'ADMIN') {
      return [
        ...commonLinks,
        { href: '/adoptions', label: 'Adoptions' },
        { href: '/users', label: 'Users' },
      ];
    }

    if (user.role === 'VOLUNTEER') {
      return [
        ...commonLinks,
        { href: '/users', label: 'Users' },
        { href: '/adoptions', label: 'Adoptions' },
      ];
    }

    if (user.role === 'ADOPTER') {
      return [
        ...commonLinks,
      ];
    }

    return commonLinks;
  };

  const links = getLinks();

  return (
    <AppShell
      header={{ height: { base: 60, md: 70, lg: 80 } }}
      navbar={{
        width: { base: 200, md: 300, lg: 400 },
        breakpoint: 'sm',
        collapsed: { mobile: !opened },
      }}
      padding="md"
    >
      <AppShell.Header>
      <Group h="100%" px="md" justify="space-between">
          <Group>
            <Burger opened={opened} onClick={toggle} hiddenFrom="sm" size="sm" />
            {user && <Text>Welcome, {user.username}</Text>}
          </Group>
          {user ? (
            <Button onClick={handleLogout}>Logout</Button>
          ) : (
            <Link href="/login">
              <Button>Login</Button>
            </Link>
          )}
        </Group>
      </AppShell.Header>
      <AppShell.Navbar p="md">
        {links.map((link) => (
          <NavLink
            key={link.href}
            component={Link}
            href={link.href}
            label={link.label}
          />
        ))}
      </AppShell.Navbar>
      <AppShell.Main>
        {children}
      </AppShell.Main>
    </AppShell>
  );
}
