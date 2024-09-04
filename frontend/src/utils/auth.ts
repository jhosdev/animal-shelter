'use server'

import { cookies } from 'next/headers'

export const setAuthTokens = async (accessToken: string | null, refreshToken: string | null) => {
  const oneDay = 24 * 60 * 60 * 1000
  const oneMinute = 60 * 60 * 1000
  if (accessToken) {
    cookies().set('accessToken', accessToken, { expires: Date.now() + oneMinute })
  } else {
    cookies().delete('accessToken')
  }

  if (refreshToken) {
    cookies().set('refreshToken', refreshToken, { expires: Date.now() + oneDay })
  } else {
    cookies().delete('refreshToken')
  }
};

export const getAccessToken = async () => {
  const cookieStore = cookies();
  return cookieStore.get('accessToken')?.value || null;
};

export const getRefreshToken = async () => {
  const cookieStore = cookies();
  return cookieStore.get('refreshToken')?.value || null;
};

export const refreshAccessToken = async () => {
  const refreshToken = await getRefreshToken();
  if (!refreshToken) return null;

  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/token/refresh/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refresh: refreshToken }),
    });

    if (response.ok) {
      const data = await response.json();
      await setAuthTokens(data.access, refreshToken);
      return data.access;
    } else {
      await setAuthTokens(null, null);
      return null;
    }
  } catch (error) {
    console.error('Error refreshing token:', error);
    await setAuthTokens(null, null);
    return null;
  }
};