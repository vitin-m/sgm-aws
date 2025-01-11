export default interface IUserData {
  description: string | null;
  full_name: string;
  hashed_password: string;
  created_at: string;
  username: string;
  email: string;
  id: string;
  profile_pic: string | null;
}
