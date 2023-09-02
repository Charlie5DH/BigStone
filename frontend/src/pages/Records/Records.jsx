import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { getTransactions, getTransactionsSummary } from "../../actions/transactions";
import { getItems } from "../../actions/items";
import { ProgressSpinner } from "primereact/progressspinner";
import Toolbar from "./components/Toolbar";
import TotalSummary from "./components/TotalSummary";
import DailySummary from "./components/DailySummary";
import StockSummary from "./components/StockSummary";

const Records = () => {
  const options = ["Hoje", "Ontem", "Últimos 7 dias", "Últimos 30 dias", "3 Mêses", "Selecione um período"];
  const viewOptions = ["Total", "Diario", "Inventário"];

  const { items, isLoadingItems } = useSelector((state) => state.items);
  const { transactions, isLoadingTransactions, isLoadingSummaryOfTransactions, transactionsSummary } = useSelector(
    (state) => state.transactions
  );

  const [viewOption, setViewOption] = React.useState(viewOptions[0]);
  const [option, setOption] = React.useState(options[2]);
  const dispatch = useDispatch();

  React.useEffect(() => {
    dispatch(getTransactions());
    dispatch(getItems(true));
    dispatch(getTransactionsSummary(option));
  }, []);

  React.useEffect(() => {
    dispatch(getTransactionsSummary(option));
  }, [option, dispatch]);

  return (
    <React.Fragment>
      {isLoadingTransactions || isLoadingItems || isLoadingSummaryOfTransactions ? (
        <div className="flex items-center justify-center mt-10 mx-4 my-2">
          <ProgressSpinner
            style={{ width: "80px", height: "80px" }}
            strokeWidth="4"
            fill="var(--surface-ground)"
            animationDuration="1.2s"
          />
        </div>
      ) : (
        <div className="flex flex-col gap-y-2 w-full">
          <Toolbar
            transactions={transactions}
            value={option}
            setValue={setOption}
            options={options}
            viewOption={viewOption}
            setViewOption={setViewOption}
            viewOptions={viewOptions}
          />

          <div
            className="flex flex-col gap-y-2 items-center mt-2 border 
          bg-white shadow-indigo-100 shadow-md rounded-md p-3 max-w-full
          overflow-x-auto mx-2 my-2 gap-4"
          >
            {viewOption === "Total" ? (
              <TotalSummary transactionsSummary={transactionsSummary} items={items} />
            ) : viewOption === "Diario" ? (
              <DailySummary transactionsSummary={transactionsSummary} items={items} />
            ) : (
              <StockSummary transactionsSummary={transactionsSummary} items={items} />
            )}
          </div>
        </div>
      )}
    </React.Fragment>
  );
};

export default Records;
