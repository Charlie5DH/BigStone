import React, { useMemo } from "react";

const meanValueOfKgPrice = (rows) => {
  const kgPrice = rows.map((row) => row.kg_price);
  const total = kgPrice.reduce((acc, value) => acc + value, 0);
  return total / kgPrice.length;
};

export const columns = (rows) => {
  return [
    {
      id: "client_name",
      accessorKey: "client_name", //access nested data with dot notation
      header: "Cliente",
      enableGrouping: true,
      Header: ({ column }) => (
        <p className="font-display dark:text-gray-200 text-slate-500 font-medium text-14">{column.columnDef.header}</p>
      ),
      Cell: ({ cell, row }) => (
        <div className="flex flex-col">
          <span className="text-slate-500 font-display font-light text-14">{cell.getValue()}</span>
          <span className="font-display font-light text-slate-500 text-12 flex dark:text-gray-200">
            {row.original.client_email}
          </span>
        </div>
      ),
    },
    {
      id: "meal_price",
      accessorKey: "meal_price", //access nested data with dot notation
      header: "Valor da Refeição",
      enableGrouping: true,
      Header: ({ column }) => (
        <span className="font-display dark:text-gray-200 text-slate-500 font-medium text-14">
          {column.columnDef.header} $R
        </span>
      ),
      Cell: ({ cell, row }) => (
        <span className="text-slate-500 font-display font-light text-14">{cell.getValue()}</span>
      ),
      Footer: () => (
        <div className="flex flex-col">
          <div className="flex flex-wrap gap-1">
            <p className="text-gray-500 font-display font-medium text-12">Total do dia</p>
            <span
              className={`font-display font-semibold text-14 ${
                rows
                  .filter((row) => row.timestamp.split("T")[0] === new Date().toISOString().split("T")[0])
                  .reduce((acc, row) => acc + row.meal_price, 0) > 0
                  ? "text-emerald-500"
                  : "text-amber-400"
              }`}
            >
              {
                // meal_price of the day (sum of all meal_price filtering by timestamp)
                rows
                  .filter((row) => row.timestamp.split("T")[0] === new Date().toISOString().split("T")[0])
                  .reduce((acc, row) => acc + row.meal_price, 0) || 0
              }
            </span>
          </div>
          <div className="flex flex-wrap gap-1">
            <p className="text-gray-500 font-display font-medium text-12">Total ontem</p>
            <span className="font-display font-semibold text-indigo-500 text-14">
              {
                // meal_price of yesterday (sum of all meal_price filtering by timestamp)
                rows
                  .filter(
                    (row) =>
                      row.timestamp.split("T")[0] ===
                      new Date(new Date().setDate(new Date().getDate() - 1)).toISOString().split("T")[0]
                  )
                  .reduce((acc, row) => acc + row.meal_price, 0) || 0
              }
            </span>
          </div>
        </div>
      ),
    },
    {
      id: "weight",
      accessorKey: "weight", //access nested data with dot notation
      header: "Peso da Refeição",
      enableGrouping: true,
      Header: ({ column }) => (
        <span className="font-display dark:text-gray-200 text-slate-500 font-medium text-14">
          {column.columnDef.header} (Kg)
        </span>
      ),
      Cell: ({ cell, row }) => (
        <span className="text-slate-500 font-display font-light text-14">{cell.getValue()}</span>
      ),
    },
    {
      id: "kg_price",
      accessorKey: "kg_price", //access nested data with dot notation
      header: "Preço do KG",
      size: 200,
      enableGrouping: true,
      Header: ({ column }) => (
        <span className="font-display dark:text-gray-200 text-slate-500 font-medium text-14">
          {column.columnDef.header}
        </span>
      ),
      Cell: ({ cell, row }) => (
        <span className="text-slate-500 font-display font-light text-14">{cell.getValue()}</span>
      ),
      Footer: () => (
        <div className="flex gap-1 items-center">
          <p className="text-gray-500 font-display font-medium text-12">Media</p>
          <div className="flex flex-wrap gap-0.5 items-center justify-center">
            <p className="font-display font-semibold text-indigo-500 text-14">{meanValueOfKgPrice(rows)}</p>
          </div>
        </div>
      ),
    },
    {
      id: "items",
      accessorKey: "items", //access nested data with dot notation
      header: "# de itens vendidos",
      enableGrouping: true,
      Header: ({ column }) => (
        <span className="font-display dark:text-gray-200 text-slate-500 font-medium text-14">
          {column.columnDef.header}
        </span>
      ),
      Cell: ({ cell, row }) => (
        <span className="text-slate-500 font-display font-light text-14">{cell.getValue().length}</span>
      ),
    },
    {
      id: "items",
      accessorKey: "items", //access nested data with dot notation
      header: "Valor dos itens vendidos",
      size: 200,
      enableGrouping: true,
      Header: ({ column }) => (
        <span className="font-display dark:text-gray-200 text-slate-500 font-medium text-14">
          {column.columnDef.header} (R)
        </span>
      ),
      Cell: ({ cell, row }) => (
        <span className="text-slate-500 font-display font-light text-14">
          {cell.getValue().reduce((acc, item) => acc + item.price * item.quantity, 0)}
        </span>
      ),
      Footer: () => (
        <div className="flex gap-1 items-center">
          <p className="text-gray-500 font-display font-medium text-12">Total hoje</p>
          <div className="flex flex-wrap gap-0.5 items-center justify-center">
            <p className="font-display font-semibold text-indigo-500 text-14">
              {
                // sum of all items price filtering by timestamp
                rows
                  .filter((row) => row.timestamp.split("T")[0] === new Date().toISOString().split("T")[0])
                  .reduce((acc, row) => acc + row.items.reduce((acc, item) => acc + item.price * item.quantity, 0), 0)
                  .toFixed(2) || 0
              }
            </p>
          </div>
        </div>
      ),
    },
    {
      id: "total",
      accessorKey: "total", //access nested data with dot notation
      header: "Valor total",
      enableGrouping: true,
      Header: ({ column }) => (
        <span className="font-display dark:text-gray-200 text-slate-500 font-medium text-14">
          {column.columnDef.header} (R)
        </span>
      ),
      Cell: ({ cell, row }) => (
        <span className="text-slate-500 font-display font-light text-14">{cell.getValue()}</span>
      ),
    },
    {
      id: "timestamp",
      accessorKey: "timestamp", //access nested data with dot notation
      header: "Data",
      enableGrouping: true,
      Header: ({ column }) => (
        <span className="font-display dark:text-gray-200 text-slate-500 font-medium text-14">
          {column.columnDef.header}
        </span>
      ),
      Cell: ({ cell, row }) => (
        <span className="text-slate-500 font-display font-light text-14">
          {cell.getValue().split("T")[0]} {cell.getValue().split("T")[1].split(".")[0]}
        </span>
      ),
    },
  ];
};

/*
{
    "_id": "64e582cfe1be677a054c8140",
    "client_id": "64d29588435382d081ba9795",
    "client_name": "John Doe",
    "client_email": "johndoe@example.com",
    "rfid": "RFID123",
    "items": [
      {
        "item_id": "64d2d745df6f0cfeed2cb223",
        "quantity": 1,
        "name": "Item 1",
        "price": 1.99
      },
      {
        "item_id": "64d2f10047614dfdea47e247",
        "quantity": 2,
        "name": "Item 2",
        "price": 1.99
      }
    ],
    "total": 5.97,
    "timestamp": "2023-08-23T03:11:04.430662",
    "kg_price": 30,
    "meal_price": 0,
    "weight": 0
  },
*/
