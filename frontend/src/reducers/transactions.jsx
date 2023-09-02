import {
  GET_TRANSACTIONS,
  GET_TRANSACTIONS_BY_ID,
  CREATE_TRANSACTION,
  UPDATE_TRANSACTION,
  DELETE_TRANSACTION,
  LOADING_TRANSACTIONS,
  END_LOADING_TRANSACTIONS,
  GET_SUMMARY_OF_TRANSACTIONS,
  LOADING_SUMMARY_OF_TRANSACTIONS,
  END_LOADING_SUMMARY_OF_TRANSACTIONS,
  GET_TRANSACTIONS_SUMMARY_BY_CLIENT,
} from "../constants/transactions";

const reducer = (
  state = {
    transactions: [],
    transactionsSummary: [],
    transactionsSummaryByClient: [],
    isLoadingSummaryOfTransactions: true,
    isLoadingTransactions: true,
  },
  action
) => {
  switch (action.type) {
    case GET_TRANSACTIONS:
      return { ...state, transactions: action.payload };
    case GET_TRANSACTIONS_BY_ID:
      return { ...state, transactions: action.payload };
    case GET_SUMMARY_OF_TRANSACTIONS:
      return { ...state, transactionsSummary: action.payload };
    case GET_TRANSACTIONS_SUMMARY_BY_CLIENT:
      return { ...state, transactionsSummaryByClient: action.payload };
    case CREATE_TRANSACTION:
      return { ...state, transactions: [...state.transactions, action.payload] };
    case UPDATE_TRANSACTION:
      return {
        ...state,
        transactions: state.transactions.map((transaction) =>
          transaction._id === action.payload._id ? action.payload : transaction
        ),
      };
    case DELETE_TRANSACTION:
      return {
        ...state,
        transactions: state.transactions.filter((transaction) => transaction._id !== action.payload),
      };
    case LOADING_TRANSACTIONS:
      return { ...state, isLoadingTransactions: true };
    case END_LOADING_TRANSACTIONS:
      return { ...state, isLoadingTransactions: false };
    case LOADING_SUMMARY_OF_TRANSACTIONS:
      return { ...state, isLoadingSummaryOfTransactions: true };
    case END_LOADING_SUMMARY_OF_TRANSACTIONS:
      return { ...state, isLoadingSummaryOfTransactions: false };
    default:
      return state;
  }
};

export default reducer;
