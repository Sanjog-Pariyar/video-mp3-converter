import axios from "axios";

export const handleUpload = async () => {

    try {
      const response = await axios.post(
        "http://localhost:8000/convert",
        {
          responseType: "blob", // important: tell axios to expect a file
        }
      );

      // Create a link to download the mp3
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
    //   link.setAttribute("download", file.name.replace(/\.[^/.]+$/, ".mp3")); // replace extension
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error(err);
      alert("Conversion failed");
    }
  };