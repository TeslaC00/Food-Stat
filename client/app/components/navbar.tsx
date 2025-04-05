import Image from "next/image";
import Link from "next/link";

export default function Navbar() {
  return (
    <div className="flex justify-between h-100px">
      {/* Left Section */}
      <div className="pl-[10px]">
        <Image
          src={"/FoodStatLogo2x1.jpg"}
          height={60}
          width={150}
          alt="FoodStat Logo"
        ></Image>
      </div>

      {/* Middle Section */}
      <div
        className="
      flex flex-1 items-center gap-10 justify-center text-black text-2xl font-medium"
      >
        <Link href={"/home"}>Home</Link>
        <Link href={"/about"}>About us</Link>
        <Link href={"/scan"}>Scan Item</Link>
        <Link href={"/contact"}>Contact us</Link>
      </div>

      {/* Right Section */}
      <div className="flex items-center pr-[10px]">
        <Link href={"/user"}>
          <Image
            src="/userBlack.png"
            height={65}
            width={65}
            alt="User Profile"
            className="rounded-full aspect-square object-cover"
          ></Image>
        </Link>
      </div>
    </div>
  );
}
