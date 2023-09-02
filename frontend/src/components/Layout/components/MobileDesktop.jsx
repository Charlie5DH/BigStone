import { useRef } from "react";
import { AiOutlineMenu } from "react-icons/ai";
import { Menu } from "primereact/menu";
import { links } from "../../../constants/links";
import { Link, useLocation } from "react-router-dom";
import { Badge } from "@mui/material";
import { BsFillCartFill } from "react-icons/bs";
import logotext4 from "../../../assets/logotext4.svg";

const MobileDesktop = () => {
  const menu = useRef(null);
  // get current location path with react-router-dom
  const location = useLocation();
  const { pathname } = location;
  const splitLocation = pathname.split("/");
  const currentLocation = splitLocation[1];

  return (
    <div className="flex items-center justify-between mx-5 gap-1 w-full">
      <Menu
        model={links
          .map((link, index) => ({
            template: () => {
              return (
                <Link
                  key={index}
                  to={link.path}
                  className={`flex items-center text-14 font-display font-normal py-1 px-3 
            hover:bg-slate-700 hover:rounded-sm hover:text-white transition-all hover:shadow-sm
            ease-in-out duration-200 cursor-pointer h-9 ${
              currentLocation === link.path.split("/")[1]
                ? "bg-slate-700 text-white rounded-sm shadow-sm"
                : "text-slate-600"
            }`}
                >
                  <div className="flex items-center gap-2">
                    <span className="text-20">{link.icon}</span>
                    <span className="capitalize">{link.label}</span>
                  </div>
                </Link>
              );
            },
          }))
          .concat(
            { separator: true },
            {
              template: () => {
                return (
                  <Link
                    to={`/profile`}
                    className="flex items-center gap-2 text-gray-300 hover:text-white transition-all ease-in-out duration-150 py-1 px-3"
                  >
                    <img
                      src="https://images.pexels.com/photos/2379004/pexels-photo-2379004.jpeg?auto=compress&cs=tinysrgb&w=1600"
                      alt="profile"
                      className="w-8 h-8 rounded-full object-cover cursor-pointer"
                    />
                    <span className="capitalize text-14 font-display font-normal text-slate-600">Usuario</span>
                  </Link>
                );
              },
            }
          )}
        popup
        ref={menu}
        id="popup_menu_left"
      />
      <img src={logotext4} className="w-32 h-12" alt="logo" />

      <div className="flex items-center gap-4">
        <div className="cursor-pointer text-gray-300 hover:text-slate-600 p-1 duration-150">
          <Badge badgeContent={4} color="secondary">
            <BsFillCartFill className="text-20" />
          </Badge>
        </div>
        <div
          onClick={(event) => menu.current.toggle(event)}
          className="flex items-center border p-2 text-gray-300 
      border-slate-700 shadow-sm cursor-pointer rounded-md
      hover:bg-slate-700 hover:text-white transition-all ease-in-out duration-150"
        >
          <AiOutlineMenu className="text-20" />
        </div>
      </div>
    </div>
  );
};

export default MobileDesktop;
