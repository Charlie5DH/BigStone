import DesktopMenu from "./components/DesktopMenu";
import MobileDesktop from "./components/MobileDesktop";

const Navbar = () => {
  return (
    <div className="flex items-center w-full bg-slate-700 shadow-md">
      <div className="hidden md:flex relative h-16 items-center justify-between w-full">
        <DesktopMenu />
      </div>
      <div className=" flex md:hidden relative h-16 items-center justify-between w-full">
        <MobileDesktop />
      </div>
    </div>
  );
};

export default Navbar;
