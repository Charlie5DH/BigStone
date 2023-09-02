/* eslint-disable react/prop-types */
import React from "react";
import { SelectButton } from "primereact/selectbutton";

const Toolbar = ({ transactions, value, setValue, options, viewOption, setViewOption, viewOptions }) => {
  return (
    <div className="flex items-center bg-white h-full max-h-40 w-full rounded-b-md border p-3 shadow-sm">
      <div className="flex flex-wrap gap-4 items-center justify-between w-full">
        <div className="flex flex-wrap items-center gap-3">
          <SelectButton value={value} onChange={(e) => setValue(e.value)} options={options} />
          <SelectButton value={viewOption} onChange={(e) => setViewOption(e.value)} options={viewOptions} />
        </div>
      </div>
    </div>
  );
};

export default Toolbar;
