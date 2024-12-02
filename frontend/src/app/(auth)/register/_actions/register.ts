"use server";

// import { redirect } from "next/navigation";
import axiosInstance from "../../../../lib/axios";
import { Buffer } from "buffer";

const registerUser = async (formData: FormData) => {
  console.log("Registering", formData);

  const { fullname, username, email, password, description, profileImage } =
    Object.fromEntries(formData.entries()) as {
      [key: string]: string | File;
    };

  if (!fullname || !username || !email || !password) {
    throw new Error("Preencha todos os campos");
  }

  let profilePicBase64 = null;

  if (profileImage && profileImage instanceof File) {
    const buffer = Buffer.from(await profileImage.arrayBuffer());
    profilePicBase64 = buffer.toString("base64");
  }

  await axiosInstance
    .post(
      "/user/signup",
      {
        email: email.toString(),
        password: password.toString(),
        username: username.toString(),
        full_name: fullname.toString(),
        description: description.toString(),
        profile_pic: profilePicBase64,
      },
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    )
    .then((response) => {
      console.log("Registration Success", response.data.toJSON());
      // redirect("/login"); // Uncomment if you want to redirect after successful registration
    })
    .catch((error) => {
      console.log("Registration Error", error.toJSON());
    });
};

export default registerUser;
