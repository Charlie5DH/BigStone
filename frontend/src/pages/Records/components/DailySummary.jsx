/* eslint-disable react/prop-types */
import React from "react";
import { Checkbox } from "../../../components";
import { MdOutlineKeyboardDoubleArrowDown } from "react-icons/md";
import { TiArrowSortedDown, TiArrowSortedUp, TiArrowUnsorted } from "react-icons/ti";

const DailySummary = ({ transactionsSummary, items, activateDropdown = true, width = "lg:w-4/5 w-full" }) => {
  const [sort, setSort] = React.useState(0);
  const [sortedTransactionsSummary, setSortedTransactionsSummary] = React.useState(transactionsSummary.daily_summary);
  const [selected, setSelected] = React.useState([]);
  const [activeDropdown, setActiveDropdown] = React.useState({});

  React.useEffect(() => {
    setSortedTransactionsSummary(transactionsSummary.daily_summary);
  }, [transactionsSummary.daily_summary]);

  const handleDropDown = (e, submenuIndex) => {
    e.preventDefault();
    setActiveDropdown((prevState) => ({
      ...prevState,
      [submenuIndex]: !prevState[submenuIndex], // Toggle active state for the clicked submenu
    }));
  };

  const handleDropDownAll = (e) => {
    e.preventDefault();
    setActiveDropdown((prevState) => {
      const newState = {};
      for (let i = 0; i < transactionsSummary.daily_summary.length; i++) {
        newState[i] = !prevState[i];
      }
      return newState;
    });
  };

  return (
    <div className={`flex flex-nowrap items-center justify-center gap-2 ${width} font-display`}>
      <div className="flex flex-col items-center border rounded-md w-full my-3">
        <div
          className="grid grid-cols-4 lg:grid-cols-5 xl:grid-cols-8 w-full items-center
           justify-between p-3 bg-slate-100"
        >
          <div className="flex items-start col-span-2 lg:col-span-2 xl:col-span-3">
            <div className="flex items-center">
              {activateDropdown && (
                <div
                  onClick={(e) => handleDropDownAll(e)}
                  className="flex p-1 mr-2 rounded-full hover:bg-slate-200 duration-200 cursor-pointer"
                >
                  <MdOutlineKeyboardDoubleArrowDown className={`text-slate-500 text-[18px] duration-200`} />
                </div>
              )}
              <div className="flex flex-nowrap items-center gap-2">
                <Checkbox
                  label={""}
                  checked={
                    selected.length === transactionsSummary.daily_summary.length && selected.length !== 0 ? true : false
                  }
                  onChange={() =>
                    setSelected(
                      selected.length === transactionsSummary.daily_summary.length && selected.length !== 0
                        ? []
                        : transactionsSummary.daily_summary.map((e) => e.date)
                    )
                  }
                  color="bg-indigo-400"
                  checkBoxSize="h-[18px] w-[18px]"
                  rounded="rounded-[4px]"
                  disabled={false}
                  font="font-normal"
                  icon={undefined}
                />
                <span className="text-[13px] font-normal text-slate-500">
                  Lucro total do periodo: <strong>$R {transactionsSummary.total_made}</strong>
                </span>
                <div
                  onClick={() => {
                    if (sort === 0) {
                      setSortedTransactionsSummary(
                        transactionsSummary.daily_summary.sort((a, b) => new Date(b.date) - new Date(a.date))
                      );
                      setSort(1);
                    } else if (sort === 1) {
                      setSortedTransactionsSummary(
                        transactionsSummary.daily_summary.sort((a, b) => new Date(a.date) - new Date(b.date))
                      );
                      setSort(2);
                    } else {
                      setSort(0);
                    }
                  }}
                  className="flex items-center justify-center gap-1 text-slate-500
             hover:text-slate-400 duration-200 cursor-pointer ml-4"
                >
                  {sort === 0 ? (
                    <TiArrowUnsorted className="text-16 font-normal text-slate-500" />
                  ) : sort === 1 ? (
                    <TiArrowSortedDown className="text-16 font-normal text-slate-500" />
                  ) : (
                    <TiArrowSortedUp className="text-16 font-normal text-slate-500" />
                  )}
                </div>
              </div>
            </div>
          </div>

          <ColumnOfList
            sort={sort}
            setSort={setSort}
            elements={transactionsSummary.daily_summary}
            sortKey="total_sells"
            defaultSortKey="date"
            columnName="Total de vendas do dia"
            hide={false}
          />

          <ColumnOfList
            sort={sort}
            setSort={setSort}
            elements={transactionsSummary.daily_summary}
            sortKey="total_made"
            defaultSortKey="date"
            columnName="Lucro total"
            hide={false}
          />

          <ColumnOfList
            sort={sort}
            setSort={setSort}
            elements={transactionsSummary.daily_summary}
            sortKey="total_by_meal"
            defaultSortKey="date"
            columnName="Total por refeição"
          />

          <ColumnOfList
            sort={sort}
            setSort={setSort}
            elements={transactionsSummary.daily_summary}
            sortKey="total_by_item"
            defaultSortKey="date"
            columnName="Total em produtos"
          />

          <ColumnOfList
            sort={sort}
            setSort={setSort}
            elements={transactionsSummary.daily_summary}
            sortKey="items_sold"
            defaultSortKey="date"
            columnName="# de produtos vendidos"
          />
        </div>

        {sortedTransactionsSummary.map((transaction, index) => (
          <div key={index} className={`flex flex-col gap-y-1 w-full px-3 py-1 duration-200 border-t hover:bg-slate-50`}>
            <div
              className="grid grid-cols-4 lg:grid-cols-5 xl:grid-cols-8 w-full items-center
           justify-between p-3"
            >
              <div className="flex items-center col-span-2 lg:col-span-2 xl:col-span-3">
                {activateDropdown && (
                  <button
                    disabled={transaction.total_made === 0}
                    onClick={(e) => handleDropDown(e, index)}
                    className={`flex mr-2 rounded-full hover:bg-slate-200 duration-200 p-0.5 ${
                      transaction.total_made === 0 ? "opacity-30 cursor-default" : "cursor-pointer"
                    }`}
                  >
                    <MdOutlineKeyboardDoubleArrowDown
                      className={`${activeDropdown[index] && "-rotate-90"} text-slate-500 text-[18px] duration-200`}
                    />
                  </button>
                )}
                <Checkbox
                  label={""}
                  checked={selected.includes(transaction.date)}
                  onChange={() => {
                    if (selected.includes(transaction.date)) {
                      setSelected(selected.filter((e) => e !== transaction.date));
                    } else {
                      setSelected([...selected, transaction.date]);
                    }
                  }}
                  color="bg-indigo-400"
                  checkBoxSize="h-[18px] w-[18px]"
                  rounded="rounded-[4px]"
                  disabled={false}
                  font="font-normal"
                  icon={undefined}
                />
                <div className="flex flex-col items-start">
                  <span className="text-14 font-medium text-slate-600">{transaction.date.split("T")[0]}</span>
                </div>
              </div>

              <div
                className="flex items-center justify-center gap-1 text-slate-500
             hover:text-slate-400 duration-200 border-l"
              >
                <span className="text-slate-500 font-display font-light text-14">{transaction.total_sells}</span>
              </div>

              <div
                className={`flex items-center justify-center gap-1 
             hover:text-slate-400 duration-200 border-l ${
               transaction.total_made > 0 ? "text-slate-500 font-light" : "text-red-400 font-normal"
             }`}
              >
                <span className="font-display text-14">$R {transaction.total_made}</span>
              </div>

              <div
                className="lg:flex hidden items-center justify-center gap-1 text-slate-500
             hover:text-slate-400 duration-200 border-l"
              >
                <span className="text-slate-500 font-display font-light text-14">$R {transaction.total_by_meal}</span>
              </div>

              <div
                className="lg:flex hidden items-center justify-center gap-1 text-slate-500
             hover:text-slate-400 duration-200 border-l"
              >
                <span className="text-slate-500 font-display font-light text-14">{transaction.total_by_item}</span>
              </div>

              <div
                className="lg:flex hidden items-center justify-center gap-1 text-slate-500
             hover:text-slate-400 duration-200 border-l"
              >
                <span className="text-slate-500 font-display font-light text-14">{transaction.items_sold}</span>
              </div>
            </div>
            {activeDropdown[index] && activateDropdown && (
              <div className="flex flex-col gap-y-1 px-3 py-2 duration-200 ml-6 border-t">
                <div className="flex flex-col w-full gap-2 border rounded-md p-3 overflow-y-scroll max-h-[400px]">
                  <span className="text-slate-700 font-secondary font-normal text-20">Relatorio de Clientes</span>
                  <div id="divider" className="border-b my-2"></div>

                  {transaction?.more_selled_items?.map((item, index) => (
                    <div key={index} className="flex items-center justify-between">
                      <div className="flex items-center">
                        <img
                          src={`http://localhost:8003/api/get_image/${
                            items.find((row) => row._id === item.item_id).image
                          }`} //"https://placehold.co/600x400" ||
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
                        <span className="text-12 font-normal text-slate-500 text-right">
                          Total vendidos: {item.quantity}
                        </span>
                        <span className="text-12 font-normal text-slate-500 text-right">
                          Preço da unidade: $R {item.price}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="flex flex-col w-full gap-2 border rounded-md p-3 overflow-y-scroll max-h-[400px]">
                  {transaction?.clients_with_more_transactions_daily?.map((item, index) => (
                    <div key={index} className="flex items-center justify-between my-1">
                      <div className="flex items-center">
                        <div className="flex flex-col items-start">
                          <span className="text-14 font-medium text-slate-700">{item.name}</span>
                          <span className="text-12 font-normal text-slate-500">{item.email}</span>
                        </div>
                      </div>
                      <div className="flex flex-col">
                        <span className="text-14 font-medium text-slate-700 text-right">Total: $R {item.total}</span>
                        <span className="text-12 font-normal text-slate-500 text-right">
                          Compras: {item.transactions}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

const ColumnOfList = ({ sort, setSort, elements, sortKey, defaultSortKey, columnName, hide = true }) => {
  return (
    <div
      onClick={() => {
        if (sort === 0) {
          // sort by price
          setSort(elements.sort((a, b) => (b[sortKey] < a[sortKey] ? -1 : b[sortKey] > a[sortKey] ? 1 : 0)));
          setSort(1);
        } else if (sort === 1) {
          // sort by[sortKey]
          setSort(elements.sort((a, b) => (b[sortKey] > a[sortKey] ? -1 : b[sortKey] < a[sortKey] ? 1 : 0)));
          setSort(2);
        } else {
          // sort by id
          setSort(elements.sort((a, b) => a[defaultSortKey].localeCompare(b[defaultSortKey])));
          setSort(0);
        }
      }}
      className={`${hide ? "lg:flex hidden" : "flex"} items-center justify-center gap-1 text-slate-500
             hover:text-slate-400 duration-200 cursor-pointer border-l`}
    >
      <span className="text-[13px] font-normal">{columnName}</span>
      {sort === 0 ? (
        <TiArrowUnsorted className="text-16 font-normal" />
      ) : sort === 1 ? (
        <TiArrowSortedDown className="text-16 font-normal" />
      ) : (
        <TiArrowSortedUp className="text-16 font-normal" />
      )}
    </div>
  );
};

export default DailySummary;
