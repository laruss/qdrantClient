import { configureStore } from '@reduxjs/toolkit';
import appReducer from 'app/slices/appSlice.ts';
import api from 'app/api';

export const store = configureStore({
    reducer: {
        app: appReducer,
        [api.reducerPath]: api.reducer,
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware({ serializableCheck: false }).concat(api.middleware),
});

export type AppDispatch = typeof store.dispatch;

export type RootState = ReturnType<typeof store.getState>;
