'use client'

import React, { createContext, useContext, useState, useEffect } from 'react';
import { PrismaClient } from '@prisma/client';
// import { auth } from '../../../auth';
// import { getServerSideProps } from './getServerSideProps';

import { getSession } from 'next-auth/react';

const prisma = new PrismaClient();

interface User {
  id: string;
  email: string;
  name: string | null;
  password: string;
  avatar: string | null;
}

interface UserContextProps {
  user: User | null;
  // setUser: React.Dispatch<React.SetStateAction<User | null>>;
}

const UserContext = createContext<UserContextProps | undefined>(undefined);

interface UserProviderProps {
  children: React.ReactNode;
}

export const UserProvider: React.FC<UserProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const fetchUser = async () => {
      const session = await getSession();

      if (session?.user?.email) {
        const userData = await prisma.user.findUnique({
          where: { email: session.user.email },
        });
        setUser(userData);
      }
    };
    fetchUser();
  }, []);

  return (
    <UserContext.Provider value={{ user }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = (): UserContextProps => {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
};