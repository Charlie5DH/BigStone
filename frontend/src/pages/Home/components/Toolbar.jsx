/* eslint-disable react/prop-types */
import { AiOutlineSearch } from "react-icons/ai";
import { GenericButton, Input } from "../../../components";
import { SelectButton } from "primereact/selectbutton";

const Toolbar = ({
  transactions,
  setVisible,
  setFilteredRecords,
  filterQuery,
  setFilterQuery,
  options,
  option,
  setOption,
}) => {
  const handleFilterItems = (e) => {
    setFilterQuery(e.target.value);
    if (e.target.value === "") {
      setFilteredRecords(transactions);
      return;
    }
    setFilteredRecords(
      transactions.filter((item) => item.client_name.toLowerCase().includes(e.target.value.toLowerCase()))
    );
  };

  return (
    <div className="flex items-center bg-white h-full max-h-40 w-full rounded-b-md border p-3 shadow-sm">
      <div className="flex flex-wrap gap-2 items-center justify-between w-full">
        <div className="flex flex-wrap items-str gap-3">
          <Input
            value={filterQuery}
            icon={<AiOutlineSearch className="text-slate-500 text-20 mr-2" />}
            onChange={(e) => handleFilterItems(e)}
            placeholder="Procurar por cliente"
          />
          <SelectButton value={option} onChange={(e) => setOption(e.value)} options={options} />
        </div>
        <div className="flex items-center gap-2">
          <GenericButton
            text="Atualizar Preço do Kg"
            color={"white"}
            bgColor={"bg-emerald-500"}
            onClick={() => setVisible(true)}
            icon={undefined}
          />
        </div>
      </div>
    </div>
  );
};

export default Toolbar;
