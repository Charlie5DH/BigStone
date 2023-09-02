import React from "react";

const Input = ({ icon, value, onChange, placeholder, type = "text" }) => {
  return (
    <div className="flex items-center border font-secondary border-slate-200 rounded-md w-full md:w-96 px-3 py-2 shadow-sm">
      {icon && icon}
      <input
        onChange={onChange}
        autoComplete="off"
        security="off"
        className="text-slate-500 w-full font-normal text-14
          focus:outline-none focus:ring-0 focus:ring-slate-300 focus:border-transparent"
        type={type}
        value={value}
        placeholder={placeholder}
      />
    </div>
  );
};

export default Input;
