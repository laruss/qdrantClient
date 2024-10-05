import ReactDOM from 'react-dom/client';
import App from './App.tsx';
import { NextUIProvider } from '@nextui-org/react';
import { Provider } from 'react-redux';
import { store } from 'app/store.ts';

import 'virtual:uno.css';
import 'react-toastify/dist/ReactToastify.css';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
    <Provider store={store}>
        <NextUIProvider>
            <App />
        </NextUIProvider>
    </Provider>
);
