export default async function ParseImageToBase64(
  file: File,
  maxSizeInBytes: number,
  allowedFormats: string[]
): Promise<string> {
  // Verifica o formato da imagem
  const fileFormat = file.type.split("/")[1];
  if (!allowedFormats.includes(fileFormat)) {
    throw new Error(
      `Formato de imagem não permitido. Formatos permitidos: ${allowedFormats.join(
        ", "
      )}`
    );
  }

  // Verifica o tamanho da imagem
  if (file.size > maxSizeInBytes) {
    throw new Error(
      `O tamanho da imagem não pode exceder ${maxSizeInBytes / 1024 / 1024} MB`
    );
  }

  // Converte a imagem para Base64
  const base64String = await convertToBase64(file);
  return base64String;
}

function convertToBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      const base64String = reader.result as string;
      const base64Data = base64String.split(",")[1]; // Remove o prefixo data:image/png;base64,
      resolve(base64Data);
    };
    reader.onerror = (error) => reject(error);
  });
}
