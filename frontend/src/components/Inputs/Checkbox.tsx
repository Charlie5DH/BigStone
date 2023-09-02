import React from "react";
import { GoCheck } from "react-icons/go";

const Checkbox = ({
  label,
  checked,
  onChange,
  icon,
  size = "normal",
  color = "bg-indigo-400",
  rounded = "rounded-md",
  checkBoxSize = "h-5 w-5",
  disabled = false,
  font = "font-regular",
}) => {
  const handleCheckboxChange = () => {
    if (disabled) return;
    onChange(!checked);
  };

  return (
    <div className={`flex items-center cursor-pointer`} onClick={handleCheckboxChange}>
      <div
        className={
          disabled
            ? `flex items-center ${checkBoxSize} border ${rounded} border-gray-300 bg-gray-100 dark:bg-gray-500
         checked:bg-blue-600 checked:border-blue-600 focus:outline-none transition duration-200
           align-top bg-no-repeat bg-center bg-contain float-left mr-2 cursor-not-allowed justify-center`
            : `flex items-center ${checkBoxSize} border ${rounded} border-gray-300 ${
                checked ? color : "bg-white dark:bg-gray-500"
              } checked:bg-blue-600 checked:border-blue-600 focus:outline-none transition duration-200
         align-top bg-no-repeat bg-center bg-contain float-left mr-2 cursor-pointer justify-center`
        }
      >
        {!disabled && icon ? (
          <span className={`h-4 w-4 text-white ${!checked && "opacity-0"}`}>{icon}</span>
        ) : (
          <GoCheck className={`h-4 w-4 text-white ${!checked && "opacity-0"}`} />
        )}
      </div>
      <div
        className={`${disabled ? "text-gray-400" : "text-gray-500"} dark:text-gray-400 ${font} ${
          size === "normal" ? "text-14" : "text-12"
        }`}
      >
        {label}
      </div>
    </div>
  );
};

export default Checkbox;
