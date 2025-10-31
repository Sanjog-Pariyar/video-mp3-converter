import { useEffect, useState } from "react";
import { getToken, removeToken } from "../api";
import { useNavigate } from "react-router-dom";
import axios from "axios";

interface User {
  id: string;
  email: string;
}

interface ProtectedData {
  current_user: User;
}

const Dashboard = () => {
  const [currentUser, setCurrentUser] = useState<ProtectedData | null>(null);
  const navigate = useNavigate();

  // Fetch current user
  useEffect(() => {
    const fetchCurrentUser = async () => {
      const token = getToken();
      if (!token) return;

      const res = await fetch("http://localhost:8081/user/me", {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (res.ok) {
        const json = await res.json();
        setCurrentUser({ current_user: json });
      } else {
        removeToken();
        navigate("/");
      }
    };

    fetchCurrentUser();
  }, [navigate]);

  const [file, setFile] = useState<File|null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
        setFile(e.target.files[0]);
    }
};

  const handleUpload = async () => {
    if (!file) return alert("Select a video first");

    const formData = new FormData();
    formData.append("video_file", file);

    try {
      const token = getToken();
      if (!token) return;
      const response = await axios.post(
        "http://localhost:8081/media/upload",

        formData,
        {
          responseType: "blob", // important: tell axios to expect a file
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      // Create a link to download the mp3
    //   const url = window.URL.createObjectURL(new Blob([response.data]));
    //   const link = document.createElement("a");
    //   link.href = url;
    //   link.setAttribute("download", file.name.replace(/\.[^/.]+$/, ".mp3")); // replace extension
    //   document.body.appendChild(link);
    //   link.click();
    //   link.remove();
    } catch (err) {
      console.error(err);
      alert("Conversion failed");
    }
  };

  const handleLogout = () => {
    removeToken();
    navigate("/");
  };

  if (!currentUser) return <p>Loading...</p>;

  return (
    <div className="p-8 max-w-4xl mx-auto space-y-8">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <button
          onClick={handleLogout}
          className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded"
        >
          Logout
        </button>
      </div>

      <p>Welcome, {currentUser.current_user.email}</p>
      <h2>Video to Audio Converter</h2>
      <input type="file" accept="video/*" onChange={handleFileChange} />
      <button onClick={handleUpload}>Convert & Download MP3</button>
    </div>
  );
};

export default Dashboard;
