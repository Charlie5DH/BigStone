import * as api from "../apis/";
import {
  GET_CLIENTS,
  GET_CLIENT,
  CREATE_CLIENT,
  UPDATE_CLIENT,
  DELETE_CLIENT,
  LOADING_CLIENTS,
  CLIENTS_FAILED,
  END_CLIENTS_LOADING,
  DELETE_CLIENTS,
  CLEAR_DEBT_CLIENTS,
} from "../constants/clients";

export const getClients = () => async (dispatch) => {
  dispatch({ type: LOADING_CLIENTS });
  try {
    const { data } = await api.getClients();
    dispatch({ type: GET_CLIENTS, payload: data });
  } catch (error) {
    dispatch({ type: CLIENTS_FAILED, payload: error });
  } finally {
    dispatch({ type: END_CLIENTS_LOADING });
  }
};

export const getClientById = (id) => async (dispatch) => {
  dispatch({ type: LOADING_CLIENTS });
  try {
    const { data } = await api.getClientById(id);
    dispatch({ type: GET_CLIENT, payload: data });
  } catch (error) {
    dispatch({ type: CLIENTS_FAILED, payload: error });
  } finally {
    dispatch({ type: END_CLIENTS_LOADING });
  }
};

export const createClient = (newClient) => async (dispatch) => {
  try {
    const { data } = await api.postClient(newClient);
    dispatch({ type: CREATE_CLIENT, payload: data });
  } catch (error) {
    dispatch({ type: CLIENTS_FAILED, payload: error });
  }
};

export const updateClient = (id, updatedClient) => async (dispatch) => {
  dispatch({ type: LOADING_CLIENTS });
  try {
    const { data } = await api.updateClient(id, updatedClient);
    dispatch({ type: UPDATE_CLIENT, payload: data });
  } catch (error) {
    dispatch({ type: CLIENTS_FAILED, payload: error });
  } finally {
    dispatch({ type: END_CLIENTS_LOADING });
  }
};

export const deleteClient = (id) => async (dispatch) => {
  dispatch({ type: LOADING_CLIENTS });
  try {
    await api.deleteClient(id);
    dispatch({ type: DELETE_CLIENT, payload: id });
  } catch (error) {
    dispatch({ type: CLIENTS_FAILED, payload: error });
  } finally {
    dispatch({ type: END_CLIENTS_LOADING });
  }
};

export const deleteClients = (ids) => async (dispatch) => {
  //dispatch({ type: LOADING_CLIENTS });
  try {
    await api.deleteClients(ids);
    dispatch({ type: DELETE_CLIENTS, payload: ids });
  } catch (error) {
    dispatch({ type: CLIENTS_FAILED, payload: error });
  }
  // finally {
  //   dispatch({ type: END_CLIENTS_LOADING });
  // }
};

export const clearDebtOfClients = (ids) => async (dispatch) => {
  // dispatch({ type: LOADING_CLIENTS });
  try {
    const { data } = await api.clearDebtOfClients(ids);
    dispatch({ type: CLEAR_DEBT_CLIENTS, payload: data });
  } catch (error) {
    dispatch({ type: CLIENTS_FAILED, payload: error });
  }
  // finally {
  //   dispatch({ type: END_CLIENTS_LOADING });
  // }
};
