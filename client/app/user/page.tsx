"use client";
import { useState, useEffect } from "react";
import { Image } from "@heroui/react";
import Navbar from "../components/navbar";
import { Profile } from "../lib/type";
import api from "../lib/api";
import { useRouter } from "next/navigation";

const calculateBMI = (weight: number, height: number) => {
  if (weight && height) {
    return (weight / (height * height)).toFixed(2);
  }
  return "";
};

async function GetUsers(): Promise<Profile[]> {
  const user_id_obj = JSON.parse(localStorage.getItem("userData") || "");
  if (user_id_obj == "") {
    return [];
  }
  const user_id = user_id_obj["id"];
  const data = await api
    .get(`/user/${user_id}/profiles`)
    .then((response) => response.data.profiles);
  return data;
}

function SaveUserProfile(user_id: string) {
  localStorage.setItem("user_profile_id", user_id);
}

export default function User() {
  const [selectedUserID, setSelectedUserID] = useState<string | undefined>(
    undefined
  );
  const [selectedUser, setSelectedUser] = useState<Profile>();
  const [users, setUsers] = useState<Profile[]>([]);
  const router = useRouter();

  useEffect(() => {
    const fetchUsers = async () => {
      const fetchedUsers = await GetUsers();
      setUsers(fetchedUsers);
    };
    fetchUsers();
  }, []);

  useEffect(() => {
    const user_id = localStorage.getItem("user_profile_id");
    if (user_id) {
      setSelectedUserID(user_id);
    }
  }, []);

  useEffect(() => {
    if (selectedUserID) {
      const user = users.find((user) => user._id === selectedUserID);
      if (user) {
        setSelectedUser(user);
      } else {
        setSelectedUser(undefined);
      }
    }
  }, [selectedUserID, users]);

  return (
    <>
      <Navbar />
      <div className="flex justify-center items-center h-screen">
        <div className="w-max bg-slate-200 p-5 rounded-lg shadow-lg mb-6 mt-8">
          <div className="flex justify-center">
            <Image
              src="https://cdn.pixabay.com/photo/2021/07/02/04/48/user-6380868_640.png"
              alt="User Image"
              width={120}
              height={120}
              className="object-cover rounded-full mb-3"
            />
          </div>
          <div className="place-self-start mb-6 ">
            <label className="block mb-1 text-black">Select User:</label>
            <select
              value={selectedUserID}
              onChange={(e) => setSelectedUserID(e.target.value)}
              className="w-full border-gray-300 text-black rounded-lg p-2"
            >
              <option value="">Select User</option>
              {users.map((user) => (
                <option key={user._id} value={`${user._id}`}>
                  {`${user.firstName} ${user.lastName}`}
                </option>
              ))}
            </select>
          </div>
          <div className="grid grid-cols-2 gap-4 text-left bg-white rounded-lg p-2">
            <div>
              <label className="block mb-1 text-black">First Name:</label>
              <input
                type="text"
                value={selectedUser?.firstName}
                // onChange={(e) => setFirstName(e.target.value)}
                placeholder="First Name"
                className="w-full border-gray-300 text-black rounded-lg p-2 bg-gray-100"
              />
            </div>

            <div>
              <label className="block mb-1 text-black">Last Name:</label>
              <input
                type="text"
                value={selectedUser?.lastName}
                // onChange={(e) => setLastName(e.target.value)}
                placeholder="Last Name"
                className="w-full border-gray-300 text-black rounded-lg p-2 bg-gray-100"
              />
            </div>

            <div>
              <label className="block mb-1 text-black">Gender:</label>
              <select
                value={selectedUser?.gender}
                // onChange={(e) => setGender(e.target.value)}
                className="w-full border-gray-300 text-black rounded-lg p-2 bg-gray-100"
              >
                <option value="">Select Gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>

            <div>
              <label className="block mb-1 text-black">Weight (kg):</label>
              <input
                type="number"
                value={selectedUser?.weight}
                // onChange={(e) => setWeight(e.target.value)}
                placeholder="Weight"
                className="w-full border-gray-300 text-black rounded-lg p-2 bg-gray-100"
              />
            </div>

            <div>
              <label className="block mb-1 text-black">Height (m):</label>
              <input
                type="number"
                value={selectedUser?.height}
                // onChange={(e) => setHeight(e.target.value)}
                placeholder="Height"
                className="w-full border-gray-300 text-black rounded-lg p-2 bg-gray-100"
              />
            </div>

            <div>
              <label className="block mb-1 text-black">BMI:</label>
              <input
                type="text"
                value={
                  selectedUser?.weight && selectedUser.height
                    ? calculateBMI(selectedUser.weight, selectedUser.height)
                    : ""
                }
                readOnly
                placeholder="BMI"
                className="w-full border-gray-300 rounded-lg text-black p-2 bg-gray-100"
              />
            </div>

            <div>
              <label className="block mb-1 text-black">Age:</label>
              <input
                type="text"
                value={selectedUser?.age ? selectedUser.age.toString() : ""}
                readOnly
                placeholder="Age"
                className="w-full border-gray-300 text-black rounded-lg p-2 bg-gray-100"
              />
            </div>

            <div>
              <label className="block mb-1 text-black">Diet Type:</label>
              <select
                value={selectedUser?.dietType}
                // onChange={(e) => setDietType(e.target.value)}
                className="w-full border-gray-300 text-black rounded-lg p-2"
              >
                <option value="">Select Diet Type</option>
                <option value="Veg">Veg</option>
                <option value="Non-Veg">Non-Veg</option>
              </select>
            </div>

            <div>
              <label className="block mb-1 text-black">Disease:</label>
              <input
                type="string"
                value={selectedUser?.diseases}
                // onChange={(e) => setWeight(e.target.value)}
                placeholder="Disease"
                className="w-full border-gray-300 text-black rounded-lg p-2 bg-gray-100"
              />
            </div>


            <div className="col-span-2">
              <label className="block mb-1 text-black">Type of User:</label>
              <select
                value={selectedUser?.userType}
                // onChange={(e) => setUserType(e.target.value)}
                className="w-full border-gray-300 text-black rounded-lg p-2"
              >
                <option value="">Select User Type</option>
                <option value="General Fitness">General Fitness</option>
                <option value="Muscle Up">Muscle Up</option>
                <option value="Weight Loss">Weight Loss</option>
                <option value="Weight Gain">Weight Gain</option>
                <option value="Pregnant Mother">Pregnant Mother</option>
                <option value="Infant">Infant</option>
              </select>
            </div>
            <div className="col-span-3">
              <label className="block mb-1 text-black">
                Allergy Information:
              </label>
              <input
                type="text"
                value={selectedUser?.allergy_info?.join(", ") || ""}
                onChange={(e) => {
                  if (selectedUser) {
                    const allergiesArray = e.target.value
                      .split(",")
                      .map((allergy) => allergy.trim());
                    setSelectedUser({
                      ...selectedUser,
                      allergy_info: allergiesArray,
                    });
                  }
                }}
                placeholder="Enter allergies separated by commas"
                className="w-full border-gray-300 text-black rounded-lg p-2 bg-gray-100"
              />
            </div>
            <button
              className="bg-blue-600"
              onClick={() => {
                if (selectedUser) {
                  SaveUserProfile(selectedUser._id);
                  router.push("/home");
                } else {
                  alert("Please select a user before saving.");
                }
              }}
            >
              Save
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
