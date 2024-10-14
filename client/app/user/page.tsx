"use client";
import { useState, useEffect } from "react";
import { Image } from "@nextui-org/image";
import { DatePicker } from "@nextui-org/date-picker";
import { CalendarDate } from "@internationalized/date";
import { Users } from "./mock_data";

const calculateBMI = (weight: number, height: number) => {
  if (weight && height) {
    return (weight / (height * height)).toFixed(2);
  }
  return "";221
};

const calculateAge = (dob: CalendarDate | null): number => {
  if (!dob) return 0;
  const birthDate = dob.toDate('UTC');
  const ageDifMs = Date.now() - birthDate.getTime();
  const ageDate = new Date(ageDifMs);
  return Math.abs(ageDate.getUTCFullYear() - 1970);
};

export default function User() {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [gender, setGender] = useState("");
  const [weight, setWeight] = useState<string>("");
  const [height, setHeight] = useState<string>("");
  const [dob, setDob] = useState<CalendarDate | null>(null);
  const [dietType, setDietType] = useState("");
  const [userType, setUserType] = useState("");
  const [selectedUser, setSelectedUser] = useState("");

  useEffect(() => {
    if (selectedUser) {
      const user = Users.find(
        (user) => `${user.firstName} ${user.lastName}` === selectedUser
      );
      if (user) {
        setFirstName(user.firstName);
        setLastName(user.lastName);
        setGender(user.gender);
        setWeight(user.weight.toString());
        setHeight(user.height.toString());
        setDob(null); // You can implement date parsing here
        setDietType(user.dietType);
        setUserType(user.userType);
      }
    }
  }, [selectedUser]);

  return (
    <div className="flex justify-center items-center h-screen ">
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
        <div className="place-self-start mb-6">
        <label className="block mb-1 text-black">Select User:</label>
        <select
          value={selectedUser}
          onChange={(e) => setSelectedUser(e.target.value)}
          className="w-full border-gray-300 text-black rounded-lg p-2"
        >
          <option value="">Select User</option>
          {Users.map((user) => (
            <option key={user._id} value={`${user.firstName} ${user.lastName}`}>
              {`${user.firstName} ${user.lastName}`}
            </option>
          ))}
        </select>
      </div>
        <div className="grid grid-cols-2 gap-4 text-left bg-white">
          <div>
            <label className="block mb-1 text-black">First Name:</label>
            <input
              type="text"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              placeholder="First Name"
              className="w-full border-gray-300 text-black rounded-lg p-2 bg-gray-100"
            />
          </div>

          <div>
            <label className="block mb-1 text-black">Last Name:</label>
            <input
              type="text"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              placeholder="Last Name"
              className="w-full border-gray-300 text-black rounded-lg p-2 bg-gray-100"
            />
          </div>

          <div>
            <label className="block mb-1 text-black">Gender:</label>
            <select
              value={gender}
              onChange={(e) => setGender(e.target.value)}
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
              value={weight}
              onChange={(e) => setWeight(e.target.value)}
              placeholder="Weight"
              className="w-full border-gray-300 text-black rounded-lg p-2 bg-gray-100"
            />
          </div>

          <div>
            <label className="block mb-1 text-black">Height (m):</label>
            <input
              type="number"
              value={height}
              onChange={(e) => setHeight(e.target.value)}
              placeholder="Height"
              className="w-full border-gray-300 text-black rounded-lg p-2 bg-gray-100"
            />
          </div>

          <div>
            <label className="block mb-1 text-black">BMI:</label>
            <input
              type="text"
              value={weight && height ? calculateBMI(parseFloat(weight), parseFloat(height)) : ""}
              readOnly
              placeholder="BMI"
              className="w-full border-gray-300 rounded-lg text-black p-2 bg-gray-100"
            />
          </div>

          <div className="col-span-2">
            <label className="block mb-1 text-black">Date of Birth:</label>
            <DatePicker className="max-w-[284px] text-black bg-gray-100" />
          </div>

          <div>
            <label className="block mb-1 text-black">Age:</label>
            <input
              type="text"
              value={dob ? calculateAge(dob) : ""}
              readOnly
              placeholder="Age"
              className="w-full border-gray-300 text-black rounded-lg p-2 bg-gray-100"
            />
          </div>

          <div>
            <label className="block mb-1 text-black">Diet Type:</label>
            <select
              value={dietType}
              onChange={(e) => setDietType(e.target.value)}
              className="w-full border-gray-300 text-black rounded-lg p-2"
            >
              <option value="">Select Diet Type</option>
              <option value="Veg">Veg</option>
              <option value="Non-Veg">Non-Veg</option>
            </select>
          </div>

          <div className="col-span-2">
            <label className="block mb-1 text-black">Type of User:</label>
            <select
              value={userType}
              onChange={(e) => setUserType(e.target.value)}
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
        </div>
      </div>
    </div>
  );
}