import React from "react";

const GenericButton = ({ text, onClick, color = "slate-500", bgColor, icon }) => {
  return (
    <button
      onClick={onClick}
      className={`flex items-center border shadow-sm rounded-md px-4 py-2 text-${color} font-display 
          font-normal text-14 transition duration-200 ease-in-out ${bgColor} hover:opacity-80`}
    >
      {icon}
      {text}
    </button>
  );
};

export default GenericButton;
