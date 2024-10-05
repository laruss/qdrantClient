import Slider from 'components/Slider';
import useGetConfig from 'app/hooks/useGetConfig.ts';
import { ToastContainer } from 'react-toastify';
import ControlPanel, { ShowControlPanelButton } from 'components/ControlPanel';
import QuickAccessPanel from 'components/QuickAccessPanel';
import Modals from 'components/Modals.tsx';

export default function App() {
    useGetConfig();

    return (
        <div className='h-[100vh] w-full relative flex flex-col overflow-hidden justify-end'>
            <ControlPanel/>
            <ShowControlPanelButton/>
            <Slider/>
            <QuickAccessPanel/>
            <Modals/>
            <ToastContainer
                hideProgressBar
                position='top-center'
                autoClose={1000}
                theme='dark'
            />
        </div>
    );
}
