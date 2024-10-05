import {useSelector} from "react-redux";
import {Input} from "@nextui-org/react";

import {selectControlPanel} from "app/slices/appSlice.ts";

import HideControlPanelButton from "./HideControlPanelButton.tsx";
import ControlPanelButton from "./ControlPanelButton.tsx";
import useControlPanelButtons from "./hooks/useControlPanelButtons.ts";
import useControlData from "./hooks/useControlData.ts";
import useInputData from "./hooks/useInputData.ts";
import useDetectIsOpen from "./hooks/useDetectIsOpen.ts";

export default function ControlPanel() {
    useDetectIsOpen();
    const controlPanelState = useSelector(selectControlPanel);
    const controlData = useControlData();
    const buttons = useControlPanelButtons(controlData);
    const inputData = useInputData(controlData);

    if (!controlPanelState.isOpen || !controlData) {
        return null;
    }

    return (
        <div className='absolute w-full bg-[#fff] bg-opacity-80 z-20'>
            <div className='h-auto p-8 relative flex flex-col justify-center items-center'>
                <div className='w-10/12 flex flex-row justify-center items-center gap-2 flex-wrap'>
                    {
                        inputData.map((input, index) => (
                            <Input key={index} {...input}/>
                        ))
                    }
                    {
                        buttons.map((button, index) => (
                            <ControlPanelButton key={index} {...button}/>
                        ))
                    }
                </div>
                <HideControlPanelButton/>
            </div>
        </div>
    );
}
