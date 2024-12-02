'use server'

import { redirect } from 'next/navigation'

import axiosInstance from '../../../../lib/axios'

export default async function LoginAction(fromData: FormData) {
  const { username, password } = Object.fromEntries(fromData.entries())

  const params = new URLSearchParams()
  params.append('username', username.toString())
  params.append('password', password.toString())
  params.append('grant_type', 'password')
  params.append('scope', '')
  params.append('client_id', '')
  params.append('client_secret', '')

    // const response = await axiosInstance.post('/login/access-token', params)
    //   console.log('Retorno aaaaaaaaaaaa', response.data)
    //   // localStorage.setItem('loginData', JSON.stringify(response.data))
    //   redirect('/home')

    await axiosInstance.post('/login/access-token', params).then((response) => {
    console.log("Retorno", response);
    localStorage.setItem('loginData', JSON.stringify(response.data));
    redirect("/home");
  })
  .catch((error) => {
    throw new Error("Erro ao fazer login");
  });

  // redirect("/home");
}
