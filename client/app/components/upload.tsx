import { useState } from "react";

export default function Upload() {
    const [image, setImage] = useState<string | null>(null); // State variable to store the image URL

    // Function to handle file input change
    const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];

        // Check if the file is a PNG or JPG
        if (file && (file.type === "image/png" || file.type === "image/jpeg")) {
        const reader = new FileReader();
        reader.onloadend = () => {
            const imageDataUrl = reader.result;

            // Ensure imageDataUrl is a string before storing
            if (typeof imageDataUrl === "string") {
            // Store in local storage
            localStorage.setItem("uploadedImage", imageDataUrl);

            // Or store in state variable
            setImage(imageDataUrl);
            }
        };
        reader.readAsDataURL(file);
        } else {
        alert("Please upload an image in PNG or JPG format.");
        }
    };

    return (
        <div>
        <div className=" text-black mb-2">
            <h1 className="text-center">Upload the nutritional label</h1>
        </div>
        <input type="file" accept=".png, .jpg, .jpeg" onChange={handleImageUpload} />

        {/* Display uploaded image */}
        {image && (
            <div>
            <h2 className="text-black">Uploaded Image:</h2>
            <img src={image} alt="Uploaded" style={{ maxWidth: "300px" }} />
            </div>
        )}
        </div>
    );
}
  