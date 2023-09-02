import React from "react";
import { AiFillEdit } from "react-icons/ai";

const ProductCarHor = ({ product }) => {
  return (
    <div className="flex flex-nowrap bg-white border shadow-sm rounded-md">
      <img
        src={`http://localhost:8003/api/get_image/${product.image}`}
        alt="product"
        className="rounded-l-md shadow-sm w-60 h-full object-cover"
      />
      <div className="flex flex-col p-3 w-full">
        <span className="text-20 font-normal text-slate-600 font-secondary leading-relaxed">{product.name}</span>

        <div className="flex items-center justify-between my-1">
          <span className="text-slate-600 font-secondary font-semibold text-12">{product.category}</span>
          <span className="text-slate-100 font-secondary font-medium text-12 px-2 py-0.5 rounded-full border bg-slate-700">
            R$ {product.price}
          </span>
        </div>

        <span className="text-slate-500 font-secondary font-normal text-14 my-2 leading-relaxed">
          {product.description}
        </span>

        <div className="flex items-center justify-between my-2 w-full gap-2">
          <div className="flex items-center">
            <span className="text-slate-600 font-secondary font-semibold text-12 px-3 py-0.5 rounded-md border bg-slate-100">
              {product.quantity} disponíveis
            </span>
          </div>

          <div className="flex items-center gap-1">
            <button className="text-slate-100 font-secondary font-semibold text-12 px-3 py-0.5 rounded-md hover:scale-105 duration-150 border bg-emerald-400">
              +
            </button>
            <button className="text-slate-600 font-secondary font-semibold text-12 px-3 py-0.5 rounded-md hover:scale-105 duration-150 border bg-slate-200">
              -
            </button>
            <button className="text-slate-600 font-secondary font-semibold text-12 px-2 py-0.5 rounded-md hover:scale-105 duration-150 border bg-slate-200">
              <AiFillEdit className="text-[18px]" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductCarHor;
