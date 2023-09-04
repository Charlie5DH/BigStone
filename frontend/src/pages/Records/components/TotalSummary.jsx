/* eslint-disable react/prop-types */
import React from "react";

const TotalSummary = ({ transactionsSummary, items, activateDropdown = true, width = "lg:w-4/5 w-full" }) => {
  return (
    <React.Fragment>
      <div className={`flex flex-wrap lg:flex-nowrap items-stretch ${width} gap-2`}>
        <div className="flex flex-col border rounded-md p-3 w-full">
          <span className="text-slate-700 font-secondary font-normal text-20">{transactionsSummary.total_sells}</span>
          <div id="divider" className="border-b my-2"></div>
          <span className="text-slate-500 font-secondary font-normal text-14">Total de vendas</span>
        </div>
        <div className="flex flex-col border rounded-md p-3 w-full">
          <span className="text-slate-700 font-secondary font-normal text-20">
            $R {Number(transactionsSummary.total_made).toFixed(2)}
          </span>
          <div id="divider" className="border-b my-2"></div>
          <span className="text-slate-500 font-secondary font-normal text-14">Lucro total</span>
        </div>
        <div className="flex flex-col border rounded-md p-3 w-full">
          <span className="text-slate-700 font-secondary font-normal text-20">
            $R {Number(transactionsSummary.total_by_meal).toFixed(2)}
          </span>
          <div id="divider" className="border-b my-2"></div>
          <span className="text-slate-500 font-secondary font-normal text-14">Total por refeição</span>
        </div>
        <div className="flex flex-col border rounded-md p-3 w-full">
          <span className="text-slate-700 font-secondary font-normal text-20">
            $R {Number(transactionsSummary.total_by_item).toFixed(2)}
          </span>
          <div id="divider" className="border-b my-2"></div>
          <span className="text-slate-500 font-secondary font-normal text-14">Total em vendas de produtos</span>
        </div>
        <div className="flex flex-col border rounded-md p-3 w-full">
          <span className="text-slate-700 font-secondary font-normal text-20">{transactionsSummary.items_sold}</span>
          <div id="divider" className="border-b my-2"></div>
          <span className="text-slate-500 font-secondary font-normal text-14"># de produtos vendidos</span>
        </div>
      </div>

      {activateDropdown && (
        <div className={`flex flex-col ${width} gap-2 border rounded-md p-3 overflow-y-scroll max-h-[400px]`}>
          <span className="text-slate-700 font-secondary font-normal text-20">Produtos mais vendidos</span>
          <div id="divider" className="border-b my-2"></div>

          {transactionsSummary?.more_selled_items?.map((item, index) => (
            <div key={index} className="flex items-center justify-between">
              <div className="flex items-center">
                <img
                  src={`http://localhost:8003/api/get_image/${items.find((row) => row._id === item.item_id).image}`} //"https://placehold.co/600x400" ||
                  alt="product"
                  className="rounded-md shadow-sm w-20 h-20 object-cover"
                />
                <div className="flex flex-col gap-y-1 ml-4">
                  <span className="text-14 font-medium text-slate-700">
                    {items.find((row) => row._id === item.item_id).name}
                  </span>
                  <span className="text-12 font-normal text-slate-500">
                    {items.find((row) => row._id === item.item_id).description}
                  </span>
                </div>
              </div>
              <div className="flex flex-col">
                <span className="text-14 font-medium text-slate-700 text-right">Total: R$ {item.total}</span>
                <span className="text-12 font-normal text-slate-500 text-right">Total vendidos: {item.quantity}</span>
                <span className="text-12 font-normal text-slate-500 text-right">Preço da unidade: $R {item.price}</span>
              </div>
            </div>
          ))}
        </div>
      )}
      {activateDropdown && (
        <div className={`flex flex-col ${width} gap-2 border rounded-md p-3`}>
          <span className="text-slate-700 font-secondary font-normal text-20">Relatorio de Clientes</span>
          <div id="divider" className="border-b my-2"></div>

          {transactionsSummary?.clients_with_more_transactions?.map((item, index) => (
            <div key={index} className="flex items-center justify-between my-1">
              <div className="flex items-center">
                <div className="flex flex-col items-start">
                  <span className="text-14 font-medium text-slate-700">{item.name}</span>
                  <span className="text-12 font-normal text-slate-500">{item.email}</span>
                </div>
              </div>
              <div className="flex flex-col">
                <span className="text-14 font-medium text-slate-700 text-right">Total: $R {item.total}</span>
                <span className="text-12 font-normal text-slate-500 text-right">Compras: {item.transactions}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </React.Fragment>
  );
};

export default TotalSummary;
