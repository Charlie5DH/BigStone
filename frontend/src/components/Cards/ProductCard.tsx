import React from "react";
import { AiFillEdit } from "react-icons/ai";

const ProductCard = ({ product, onButtonClick }) => {
  return (
    <div className="flex flex-col bg-white p-3 border shadow-sm rounded-md">
      <img
        src={`http://localhost:8003/api/get_image/${product.image}`}
        alt="product"
        className="rounded-md shadow-md w-full h-[400px] object-cover"
      />

      <div className="flex items-center justify-between mt-4">
        <span className="text-16 font-medium text-slate-500 font-display">{product.name}</span>
        <span className="text-16 font-medium text-slate-500 font-display">R$ {product.price}</span>
      </div>

      <span className="text-slate-500 font-display font-light text-14 my-2 italic">{product.category}</span>

      <span className="text-slate-500 font-display font-light text-14 mt-2">{product.description}</span>

      <div className="flex items-center justify-between my-2">
        <div className="flex items-center">
          <span className="text-slate-600 font-display font-semibold text-12 px-3 py-1 rounded-md border bg-slate-200">
            {product.quantity}
          </span>
        </div>
        <div className="flex items-center">
          <button
            onClick={onButtonClick}
            className="text-slate-100 font-display font-semibold text-14 px-3 py-1.5 rounded-md hover:scale-105 duration-150 border bg-emerald-500"
          >
            + Reabastecer
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;
