/* eslint-disable no-unused-vars */
/* eslint-disable react/prop-types */
import React from "react";
import Checkbox from "../Inputs/Checkbox";
import { TiArrowSortedDown, TiArrowSortedUp, TiArrowUnsorted } from "react-icons/ti";
import { IoMdTime } from "react-icons/io";
import { MdOutlineKeyboardDoubleArrowDown } from "react-icons/md";
import moment from "moment";
import "moment/locale/pt-br"; // Import Portuguese locale
import FoldableFooter from "../../pages/Home/components/foldableFooter";

// Optionally, you can set the locale globally for your application
moment.locale("pt-br");

const RecordsList = ({ records, produtos }) => {
  const [sort, setSort] = React.useState(0);
  const [sortedRecords, setSortedRecords] = React.useState(records);
  const [selected, setSelected] = React.useState([]);
  const [activeDropdown, setActiveDropdown] = React.useState({
    0: 1,
  });

  React.useEffect(() => {
    setSortedRecords(records);
  }, [records]);

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
      for (let i = 0; i < records.length; i++) {
        newState[i] = !prevState[i];
      }
      return newState;
    });
  };

  return (
    <div className="flex flex-nowrap items-center justify-center gap-2 w-full lg:w-[90%] font-display">
      <div className="flex flex-col items-center border rounded-md w-full my-3">
        <div
          className="grid grid-cols-3 sm:grid-cols-5 lg:grid-cols-8 xl:grid-cols-10 w-full items-center
           justify-between p-3 bg-slate-100"
        >
          <div className="flex items-start col-span-2 lg:col-span-2 xl:col-span-3">
            <div className="flex items-center">
              <div
                onClick={(e) => handleDropDownAll(e)}
                className="flex p-1 mr-2 rounded-full hover:bg-slate-200 duration-200 cursor-pointer"
              >
                <MdOutlineKeyboardDoubleArrowDown className={`text-slate-500 text-[18px] duration-200`} />
              </div>
              <div className="flex flex-wrap items-start gap-2">
                <Checkbox
                  label={""}
                  checked={selected.length === records.length && selected.length !== 0 ? true : false}
                  onChange={() =>
                    setSelected(
                      selected.length === records.length && selected.length !== 0 ? [] : records.map((e) => e._id)
                    )
                  }
                  color="bg-indigo-400"
                  checkBoxSize="h-[18px] w-[18px]"
                  rounded="rounded-[4px]"
                  disabled={false}
                  font="font-normal"
                  icon={undefined}
                />
                <div className="flex flex-wrap items-start gap-1">
                  <p className="text-slate-500 font-display font-normal text-[13px]">Transações dos clientes</p>
                </div>
              </div>
            </div>
          </div>

          <div
            onClick={() => {
              if (sort === 0) {
                // sort by price
                setSortedRecords([...records].sort((a, b) => (b.price < a.price ? -1 : b.price > a.price ? 1 : 0)));
                setSort(1);
              } else if (sort === 1) {
                // sort by price
                setSortedRecords([...records].sort((a, b) => (b.price > a.price ? -1 : b.price < a.price ? 1 : 0)));
                setSort(2);
              } else {
                // sort by id
                setSortedRecords([...records].sort((a, b) => a._id.localeCompare(b._id)));
                setSort(0);
              }
            }}
            className="lg:flex hidden items-center justify-center gap-1 text-slate-500
             hover:text-slate-400 duration-200 cursor-pointer border-l"
          >
            <span className="text-[13px] font-normal">Valor da Refeição</span>
            {sort === 0 ? (
              <TiArrowUnsorted className="text-16 font-normal" />
            ) : sort === 1 ? (
              <TiArrowSortedDown className="text-16 font-normal" />
            ) : (
              <TiArrowSortedUp className="text-16 font-normal" />
            )}
          </div>

          <div
            onClick={() => {
              if (sort === 0) {
                // sort by price
                setSortedRecords([...records].sort((a, b) => (b.weight < a.weight ? -1 : b.weight > a.weight ? 1 : 0)));
                setSort(1);
              } else if (sort === 1) {
                // sort by weight
                setSortedRecords([...records].sort((a, b) => (b.weight > a.weight ? -1 : b.weight < a.weight ? 1 : 0)));
                setSort(2);
              } else {
                // sort by id
                setSortedRecords([...records].sort((a, b) => a._id.localeCompare(b._id)));
                setSort(0);
              }
            }}
            className="flex items-center justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 cursor-pointer border-l"
          >
            <span className="text-[13px] font-normal">Peso da Refeição</span>
            {sort === 0 ? (
              <TiArrowUnsorted className="text-16 font-normal" />
            ) : sort === 1 ? (
              <TiArrowSortedDown className="text-16 font-normal" />
            ) : (
              <TiArrowSortedUp className="text-16 font-normal" />
            )}
          </div>

          <div className="sm:flex hidden items-center col-span-1 justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 cursor-pointer border-l">
            <span className="text-[13px] font-normal">Preço do KG</span>
          </div>

          <div className="xl:flex hidden items-center justify-center gap-1 col-span-1 text-slate-500 hover:text-slate-400 duration-200 cursor-pointer border-l">
            <span className="text-[13px] font-normal"># de itens vendidos</span>
          </div>

          <div className="xl:flex hidden items-center justify-center gap-1 col-span-1 text-slate-500 hover:text-slate-400 duration-200 cursor-pointer border-l">
            <span className="text-[13px] font-normal ml-1">Valor dos itens vendidos</span>
          </div>

          <div
            onClick={() => {
              if (sort === 0) {
                // sort by price
                setSortedRecords([...records].sort((a, b) => (b.total < a.total ? -1 : b.total > a.total ? 1 : 0)));
                setSort(1);
              } else if (sort === 1) {
                // sort by total
                setSortedRecords([...records].sort((a, b) => (b.total > a.total ? -1 : b.total < a.total ? 1 : 0)));
                setSort(2);
              } else {
                // sort by id
                setSortedRecords([...records].sort((a, b) => a._id.localeCompare(b._id)));
                setSort(0);
              }
            }}
            className="xl:flex hidden items-center justify-center gap-1 col-span-1 text-slate-500 hover:text-slate-400 duration-200 cursor-pointer border-l"
          >
            <span className="text-[13px] font-normal">Valor total</span>
            {sort === 0 ? (
              <TiArrowUnsorted className="text-16 font-normal" />
            ) : sort === 1 ? (
              <TiArrowSortedDown className="text-16 font-normal" />
            ) : (
              <TiArrowSortedUp className="text-16 font-normal" />
            )}
          </div>

          <div
            onClick={() => {
              if (sort === 0) {
                setSortedRecords(
                  [...records].sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())
                );
                setSort(1);
              } else if (sort === 1) {
                setSortedRecords(
                  [...records].sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime())
                );
                setSort(2);
              } else {
                setSortedRecords([...records].sort((a, b) => a._id.localeCompare(b._id)));
                setSort(0);
              }
            }}
            className="lg:flex hidden items-center justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 cursor-pointer border-l"
          >
            <IoMdTime className="text-20 font-normal" />
            <span className="text-[13px] font-normal">Data</span>
            {sort === 0 ? (
              <TiArrowUnsorted className="text-16 font-normal" />
            ) : sort === 1 ? (
              <TiArrowSortedDown className="text-16 font-normal" />
            ) : (
              <TiArrowSortedUp className="text-16 font-normal" />
            )}
          </div>
        </div>

        {sortedRecords.map((record, index) => (
          <div
            key={index}
            className={`flex flex-col gap-y-1 w-full px-3 py-2 duration-200
            ${index === 0 ? "border border-indigo-200 shadow-sm shadow-indigo-200" : "border-t hover:bg-slate-50"}`}
          >
            <div className="grid grid-cols-3 sm:grid-cols-5 lg:grid-cols-8 xl:grid-cols-10 items-center justify-between">
              <div className="flex items-center col-span-2 lg:col-span-2 xl:col-span-3 cursor-pointer">
                <div
                  onClick={(e) => handleDropDown(e, index)}
                  className="flex p-1 mr-2 rounded-full hover:bg-slate-200 duration-200 cursor-pointer"
                >
                  <MdOutlineKeyboardDoubleArrowDown
                    className={`${activeDropdown[index] && "-rotate-90"} text-slate-500 text-[18px] duration-200`}
                  />
                </div>
                <Checkbox
                  label={""}
                  checked={selected.includes(record._id)}
                  onChange={() => {
                    if (selected.includes(record._id)) {
                      setSelected(selected.filter((e) => e !== record._id));
                    } else {
                      setSelected([...selected, record._id]);
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
                  <span className="text-14 font-medium text-slate-700">{record.client_name}</span>
                  <span className="text-12 font-normal text-slate-500">{record.client_email}</span>
                </div>
              </div>

              <div className="lg:flex hidden items-center justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 border-l">
                <span className="text-slate-500 font-display font-light text-14">
                  $R {Number(record.meal_price).toFixed(2)}
                </span>
              </div>

              <div className="lg:flex lg:flex-col gap-y-1 hidden items-center justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 border-l">
                <span className="text-slate-500 font-display font-light text-14">{record.weight} Kg</span>
              </div>

              <div className="lg:flex hidden items-center justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 border-l col-span-1">
                <span className="text-slate-500 font-display font-light text-14">$R {record.kg_price}</span>
              </div>

              <div className="lg:flex hidden items-center justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 border-l col-span-1">
                <span className="text-slate-500 font-display font-light text-14">{record.items.length}</span>
              </div>

              <div className="lg:flex hidden items-center justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 border-l col-span-1">
                <span className="text-slate-500 font-display font-light text-14">
                  $R {record.items.reduce((acc, item) => acc + item.price * item.quantity, 0)}
                </span>
              </div>

              <div className="lg:flex hidden items-center justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 border-l col-span-1">
                <span className="text-slate-500 font-display font-light text-14">
                  $R {Number(record.total).toFixed(2)}
                </span>
              </div>

              <div className="lg:flex hidden items-center justify-center gap-1 text-slate-500 hover:text-slate-400 duration-200 border-l">
                <span className="text-14 font-normal">{moment(record.timestamp).format("lll")}</span>
              </div>
            </div>
            <FoldableFooter activeDropdown={activeDropdown} index={index} record={record} produtos={produtos} />
          </div>
        ))}
      </div>
    </div>
  );
};

export default RecordsList;
