import * as api from "../apis/";
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

export const getTransactions = (transaction_type, start_timestamp, end_timestamp) => async (dispatch) => {
  try {
    dispatch({ type: LOADING_TRANSACTIONS });
    const { data } = await api.getTransactions(transaction_type, start_timestamp, end_timestamp);
    console.log(data);
    dispatch({ type: GET_TRANSACTIONS, payload: data });
    dispatch({ type: END_LOADING_TRANSACTIONS });
  } catch (error) {
    console.log(error);
  }
};

export const getTransactionById = (id) => async (dispatch) => {
  try {
    dispatch({ type: LOADING_TRANSACTIONS });
    const { data } = await api.getTransactionById(id);
    dispatch({ type: GET_TRANSACTIONS_BY_ID, payload: data });
    dispatch({ type: END_LOADING_TRANSACTIONS });
  } catch (error) {
    console.log(error);
  }
};

export const createTransaction = (newTransaction) => async (dispatch) => {
  try {
    const { data } = await api.createTransaction(newTransaction);
    dispatch({ type: CREATE_TRANSACTION, payload: data });
  } catch (error) {
    console.log(error);
  }
};

export const updateTransaction = (id, updatedTransaction) => async (dispatch) => {
  try {
    dispatch({ type: LOADING_TRANSACTIONS });
    const { data } = await api.updateTransaction(id, updatedTransaction);
    dispatch({ type: UPDATE_TRANSACTION, payload: data });
    dispatch({ type: END_LOADING_TRANSACTIONS });
  } catch (error) {
    console.log(error);
  }
};

export const deleteTransaction = (id) => async (dispatch) => {
  try {
    await api.deleteTransaction(id);
    dispatch({ type: DELETE_TRANSACTION, payload: id });
  } catch (error) {
    console.log(error);
  }
};

export const getTransactionsSummary = (period) => async (dispatch) => {
  try {
    dispatch({ type: LOADING_SUMMARY_OF_TRANSACTIONS });
    const { data } = await api.getSummaryOfTransactions(period);
    dispatch({ type: GET_SUMMARY_OF_TRANSACTIONS, payload: data });
    dispatch({ type: END_LOADING_SUMMARY_OF_TRANSACTIONS });
  } catch (error) {
    console.log(error);
  }
};

export const getTransactionsSummaryByClient = (client_id, period) => async (dispatch) => {
  try {
    dispatch({ type: LOADING_SUMMARY_OF_TRANSACTIONS });
    const { data } = await api.getTransactionsSummaryByClient(client_id, period);
    dispatch({ type: GET_TRANSACTIONS_SUMMARY_BY_CLIENT, payload: data });
    dispatch({ type: END_LOADING_SUMMARY_OF_TRANSACTIONS });
  } catch (error) {
    console.log(error);
  }
};
