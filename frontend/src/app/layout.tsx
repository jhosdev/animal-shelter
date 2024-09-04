import "@mantine/core/styles.css";
import '@mantine/notifications/styles.css';
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { ColorSchemeScript, MantineProvider } from "@mantine/core";
import { theme } from "@/theme";

import { Notifications } from '@mantine/notifications';

import { Provider } from 'jotai';

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Animal Shelter",
  description: "Tech test for a fictional animal shelter",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <ColorSchemeScript />
        <link rel="shortcut icon" href="/favicon.svg" />
        <meta
          name="viewport"
          content="minimum-scale=1, initial-scale=1, width=device-width, user-scalable=no"
        />
      </head>
      <body className={inter.className = 'min-h-screen min-w-screen'}>
        <MantineProvider theme={theme}>
          <Notifications />
          <Provider>
              {children}
          </Provider>
        </MantineProvider>
      </body>
    </html>
  );
}
