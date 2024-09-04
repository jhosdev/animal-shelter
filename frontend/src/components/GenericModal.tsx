// components/GenericModal.tsx

import { Modal, TextInput, Button, Group, Select } from '@mantine/core';
import { useState, useEffect } from 'react';

type Field = {
  type: 'text' | 'number' | 'select' | 'date';
  label: string;
  editable: boolean;
  only_editable?: boolean;
  options?: { value: string; label: string }[];
};

interface GenericModalProps<T> {
  opened: boolean;
  onClose: () => void;
  onSubmit: (data: T) => void;
  fields: {
    [K in keyof T]: Field;
  };
  initialValues?: T;
}

export default function GenericModal<T>({
  opened,
  onClose,
  onSubmit,
  fields,
  initialValues = {} as T
}: GenericModalProps<T>) {
  const [values, setValues] = useState<any>(initialValues);
  const [errors, setErrors] = useState<{[key: string]: string}>({});

  useEffect(() => {
    setValues(initialValues);
  }, [initialValues]);

  const handleChange = (key: keyof T, value: any) => {
    setValues((prev:any) => ({ ...prev, [key]: value }));
    setErrors((prev) => ({ ...prev, [key]: '' }));
  };

  

  const validateForm = (): boolean => {
    const newErrors: {[key: string]: string} = {};
    let isValid = true;
    let hasChanges = false;

    Object.entries(fields).forEach(([key, field]) => {
      const typedField = field as Field;
      const value = values[key];
      const initialValue = initialValues[key as keyof T];

      // Check if it's a new record or an editable field
      if (typedField.editable) {
        // Check for required fields

        if (value === undefined || value === null || value === '') {
          newErrors[key] = 'This field is required';
          console.log('required', key)
          isValid = false;
        }

        // Check for changes in existing records
        if ((initialValues as any).id && value !== initialValue) {
          hasChanges = true;
        }

        if (typedField.only_editable === true && !(initialValues as any).id) {
          isValid = true;
        }
      }
    });
    console.log(initialValues)
    console.log(hasChanges)
    console.log(isValid)
    // For existing records, ensure there are changes
    if ((initialValues as any).id && !hasChanges) {
      isValid = false;
    }

    setErrors(newErrors);
    return isValid;
  };

  const handleSubmit = () => {
    console.log('values', values);
    if (validateForm()) {
      onSubmit(values);
      setErrors({});
      onClose();
    }
  };

  return (
    <Modal opened={opened} onClose={onClose} title="Manage Item">
      {Object.entries(fields).map(([key, field]) => {
        const typedField = field as Field;

        return (
          <div key={key}>
            {typedField.type === 'text' && (((initialValues as any).id && typedField.only_editable===true) || typedField.only_editable === undefined) && (
              <TextInput
                label={typedField.label}
                value={values[key] as any}
                onChange={(e) => handleChange(key as keyof T, e.currentTarget.value)}
                disabled={!typedField.editable} // Desactiva el campo si no es editable
                error={errors[key]}
                required={typedField.editable}
              />
            )}
            {typedField.type === 'number' && (((initialValues as any).id && typedField.only_editable===true) || typedField.only_editable === undefined ) && (
              <TextInput
                label={typedField.label}
                type="number"
                value={values[key] as any}
                onChange={(e) => handleChange(key as keyof T, Number(e.currentTarget.value))}
                disabled={!typedField.editable} // Desactiva el campo si no es editable
                error={errors[key]}
                required={typedField.editable}
              />
            )}
            {typedField.type === 'select' && (((initialValues as any).id && typedField.only_editable===true) || typedField.only_editable === undefined ) && typedField.options && (
              <Select
                label={typedField.label}
                value={values[key] as any}
                onChange={(value) => handleChange(key as keyof T, value)}
                data={typedField.options}
                disabled={!typedField.editable} // Desactiva el campo si no es editable
                error={errors[key]}
                required={typedField.editable}
              />
            )}
          </div>
        );
      })}
      <Group mt="md">
        <Button onClick={handleSubmit}>Submit</Button>
        <Button onClick={onClose} variant="outline">Cancel</Button>
      </Group>
    </Modal>
  );
}
