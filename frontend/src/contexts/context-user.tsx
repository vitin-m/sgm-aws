'use client'

import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

interface User {
  full_name: string | null;
  user_name: string; 
  email: string;
  password: string;
  description: string;
  profile_pic: string | null;
}

interface UserContextProps {
  user: User | null;
}

const UserContext = createContext<UserContextProps | undefined>(undefined);

interface UserProviderProps {
  children: React.ReactNode;
}

export const UserProvider: React.FC<UserProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const fetchUser = async () => {
      const loginData = localStorage.getItem('loginData');
      if (loginData) {
        const parsedData = JSON.parse(loginData);
        try {
          const response = await axios.get('/user/me', {
            headers: {
              Authorization: `Bearer ${parsedData.access_token}`,
            },
          });
          setUser(response.data);
        } catch (error) {
          console.error('Erro ao buscar usuário', error);
        }
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