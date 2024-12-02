'use server'

import { auth } from '@/../../auth';
export async function getServerSideProps() {
  const session = await auth();
  return {
    session
  };
}