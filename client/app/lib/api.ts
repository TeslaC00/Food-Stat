import axios from "axios";

const REGISTER_URL = "http://localhost:5000/sign_up"; // Adjust if needed
const LOGIN_URL = "http://localhost:5000/login"; // Adjust if needed

interface UserCredentials {
  username: string;
  password: string;
}

interface ApiResponse {
  id: string;
}

export const registerUser = async (
  credentials: UserCredentials
): Promise<ApiResponse> => {
  const response = await axios.post(REGISTER_URL, credentials);
  return response.data;
};

export const loginUser = async (
  credentials: UserCredentials
): Promise<ApiResponse> => {
  const response = await axios.post(LOGIN_URL, credentials);
  return response.data;
};

const api = axios.create({
  baseURL: "http://localhost:5000/api",
  headers: {
    "Access-Control-Allow-Origin": "*",
  },
});

export default api;
