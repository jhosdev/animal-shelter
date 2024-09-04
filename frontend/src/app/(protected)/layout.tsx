import { Shell } from "@/components/Layout";



export default function Layout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <Shell>
        {children}
    </Shell>
  );
}
