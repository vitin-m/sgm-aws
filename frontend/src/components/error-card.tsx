'use client';

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Button, buttonVariants } from '@/components/ui/button';

import Link from 'next/link';
import { cn } from '@/lib/utils';
import { CircleX } from 'lucide-react';

export default function ErrorCard({
  errorMessage,
  reset,
}: {
  errorMessage: string;
  reset: () => void;
}) {
  return (
    <>
      <div className='flex flex-col items-center justify-center h-screen'>
        <Card className="mx-auto max-w-96 border-primary bg-background">
          <CardHeader>
            <CardTitle className="flex items-center justify-center gap-2 text-primary">
              <CircleX size={20}/>
              Ops, ocorreu um problema
            </CardTitle>
            <CardDescription>Por favor, verifique o erro e tente novamente</CardDescription>
          </CardHeader>
          <CardContent className="underline">Erro: {errorMessage}</CardContent>
          <CardFooter className="flex justify-center">
            <Button variant={'outline'} onClick={reset}>
              Tentar novamente
            </Button>
          </CardFooter>
        </Card>
        <Link
          className={cn(buttonVariants({ variant: 'link' }), 'mt-8')}
          href="/"
        >
          Voltar para Home
        </Link>
      </div>
    </>
  );
}