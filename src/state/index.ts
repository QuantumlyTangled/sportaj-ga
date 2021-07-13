import { applyMiddleware, combineReducers, createStore } from '@reduxjs/toolkit';
import { composeWithDevTools } from 'redux-devtools-extension';
import createSagaMiddleware from 'redux-saga';
import userReducer from 'state/reducers/user';

const sagaMiddleware = createSagaMiddleware();

export const reducers = combineReducers({
	user: userReducer
});

export const store = createStore(reducers, composeWithDevTools({ trace: true })(applyMiddleware(sagaMiddleware)));

export type RootState = ReturnType<typeof store.getState>;
