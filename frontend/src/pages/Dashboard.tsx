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

const API_URL = "/user"

const Dashboard = () => {
  const [currentUser, setCurrentUser] = useState<ProtectedData | null>(null);
  const [mp3Id, setMp3Id] = useState("");
  const navigate = useNavigate();

  // Fetch current user
  useEffect(() => {
    const fetchCurrentUser = async () => {
      const token = getToken();
      if (!token) return;

      const res = await fetch(`${API_URL}/me`, {
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

  const [file, setFile] = useState<File | null>(null);

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
      await axios.post(
        `${API_URL}/media/upload`,
        formData,
        {
          responseType: "blob", // important: tell axios to expect a file
          headers: { Authorization: `Bearer ${token}` },
        }
      );
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

  const handleDownload = async () => {
    try {
      const token = getToken();
      const response = await axios.get(
        `${API_URL}/media/download?mp3_fid=${mp3Id}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
          responseType: "blob", // Important: so browser treats it as a file
        }
      );

      // Extract filename from response header if present
      const disposition = response.headers["content-disposition"];
      let filename = "converted_audio.mp3";
      if (disposition) {
        const match = disposition.match(/filename="(.+)"/);
        if (match?.[1]) filename = match[1];
      }

      // Create a temporary download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();

      // Cleanup
      a.remove();
      window.URL.revokeObjectURL(url);
      setMp3Id("")
    } catch (error: any) {
      console.error("❌ Download failed:", error);
      alert("Download failed. Please try again.");
    }
  };

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
      <input
        type="text"
        value={mp3Id}
        onChange={(e) => setMp3Id(e.target.value)}
        placeholder="Enter MP3 File ID..."
        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button
        onClick={handleDownload}
        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg shadow"
      >
        Download MP3
      </button>
    </div>
  );
};

export default Dashboard;
