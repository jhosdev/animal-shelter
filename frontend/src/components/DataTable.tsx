// components/DataTable.tsx

import { Table, Group, Text } from '@mantine/core';
import { format } from 'date-fns';

interface DataTableProps<T> {
  data: T[];
  columns: string[];
  actions?: (item: T) => JSX.Element[];
  typeLabels?: {
    [key: string]: {
      [key: string]: string;
    };
  };
}

const formatDate = (dateString: string) => {
  try {
    const date = new Date(dateString);
    return format(date, 'HH:mm') + ' ' + format(date, 'dd-MM-yyyy');
  } catch (error) {
    return dateString; // En caso de error, devolver la fecha sin formatear
  }
};

export default function DataTable<T>({
  data,
  columns,
  actions,
  typeLabels,
}: DataTableProps<T>) {

  if (data.length === 0) {
    return <Text>There are no records to display.</Text>;
  }

  return (
    <Table>
      <Table.Thead>
        <Table.Tr>
          {columns.map((col, idx) => (
            <Table.Th key={idx}>{col}</Table.Th>
          ))}
          {actions && actions(data[0])?.length > 0 && <Table.Th>Actions</Table.Th>}
        </Table.Tr>
      </Table.Thead>
      <Table.Tbody>
        {data.map((item, idx) => (
          <Table.Tr key={idx}>
            {Object.entries(item as any).map(([key, value], idx) => (
              <Table.Td key={idx}>
                {key === 'date' && typeof value === 'string'
                  ? formatDate(value)
                  : typeLabels && typeLabels[key] && typeLabels[key][value as string]
                    ? typeLabels[key][value as string]
                    : value as any}
              </Table.Td>
            ))}
            {actions && actions(item)?.length > 0 && (
              <Table.Td>
                <Group gap="xs">
                  {actions(item)}
                </Group>
              </Table.Td>
            )}
          </Table.Tr>
        ))}
      </Table.Tbody>
    </Table>
  );
}
