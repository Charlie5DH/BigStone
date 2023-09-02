import React from "react";

function Card({ title, subtitle, titleCompare, footer, sign = "+" }) {
  return (
    <div className="flex flex-col rounded-md border shadow-indigo-100 p-4 bg-white w-full font-secondary">
      <div className="flex flex-row justify-between">
        <div className="flex flex-col w-full">
          <div className="flex items-center justify-between gap-2">
            <span className="text-slate-600 font-bold text-20">{title}</span>

            {titleCompare && (
              <div
                className={`flex items-center px-2 py-0.5 uppercase text-slate-50 text-12 
              font-normal border rounded-full shadow-sm ${sign === "+" ? "bg-emerald-400" : "bg-red-300"}`}
              >
                {titleCompare}
              </div>
            )}
          </div>

          <div className="w-[90%] bg-slate-200 h-[1px] rounded-full my-1" />
          <span className="text-gray-500 text-14 font-light uppercase">{subtitle}</span>
        </div>
      </div>

      {footer && footer}
    </div>
  );
}

export default Card;

// Path: frontend\src\components\Cards\Card.tsx
