import { atomWithStorage } from 'jotai/utils';
import { User } from '@/utils/types';

export const userAtom = atomWithStorage<User | null>('user',null);
