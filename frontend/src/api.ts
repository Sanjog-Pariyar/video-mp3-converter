const API_URL = "/user";

export interface LoginResponse {
  access_token: string;
}

export const login = async (
  email: string,
  password: string
): Promise<LoginResponse> => {
  const formData = new URLSearchParams();
  formData.append("email", email);
  formData.append("password", password);
  const res = await fetch(`${API_URL}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: formData.toString()
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Login failed: ${text}`);
  }

  const tokenData = await res.json();

  return tokenData.data;
};

export const getToken = (): string | null => localStorage.getItem("token");
export const setToken = (token: string): void =>
  localStorage.setItem("token", token);
export const removeToken = (): void => localStorage.removeItem("token");

export const test = async () => {
  await fetch(API_URL);
};

export const register = async (email: string, password: string) => {
  const res = await fetch(`${API_URL}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      email,
      password,
    }),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Login failed: ${text}`);
  }

  return await res.json();
};
