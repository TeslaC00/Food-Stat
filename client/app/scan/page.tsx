"use client";
import { useState } from "react";
import Content1 from "../components/upload";
import Content2 from "../components/form_upload";

export default function IndexPage() {
  const [activeButton, setActiveButton] = useState("button1");
  const [content, setContent] = useState(<Content1 />);

  const handleButtonClick = (buttonId: string) => {
    setActiveButton(buttonId);
    switch (buttonId) {
      case "button1":
        setContent(<Content1 />);
        break;
      case "button2":
        setContent(<Content2 />);
        break;
      default:
        setContent(<div>Unknown button</div>);
    }
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gray-200 rounded-xl m-2">
      <div className="bg-white rounded-lg shadow-xl w-96 p-5 border-black">
        {/* Button Section */}
        <div className="flex justify-around mb-4">
          <button
            className={`${
              activeButton === "button1" ? "bg-yellow-500" : "bg-gray-300"
            } text-black px-4 py-2 border border-gray-400 rounded-md`}
            onClick={() => handleButtonClick("button1")}
          >
            Upload
          </button>
          <button
            className={`${
              activeButton === "button2" ? "bg-yellow-500" : "bg-gray-300"
            } text-black px-4 py-2 border border-gray-400 rounded-md`}
            onClick={() => handleButtonClick("button2")}
          >
            Form
          </button>
        </div>

        {/* Content Section */}
        <div className="border rounded-lg p-4">
          {content}
        </div>
      </div>
    </div>
  );
}
