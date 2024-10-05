import {Button, Tooltip} from "@nextui-org/react";
import {LuLayoutPanelTop} from "react-icons/lu";
import {useDispatch, useSelector} from "react-redux";
import {selectControlPanel, setControlPanelIsOpen} from "app/slices/appSlice.ts";

export default function ShowControlPanelButton() {
    const dispatch = useDispatch();
    const controlPanelState = useSelector(selectControlPanel);

    const handleClick = () => {
        dispatch(setControlPanelIsOpen(true));
    };

    if (controlPanelState.isOpen) {
        return null;
    }

    return (
        <div className='absolute bottom-5 left-1/2 z-20'>
            <Tooltip content='Show Control Panel'>
                <Button isIconOnly className='opacity-50 hover:opacity-70 cursor-pointer' onPress={handleClick}>
                    <LuLayoutPanelTop />
                </Button>
            </Tooltip>
        </div>
    );
}
