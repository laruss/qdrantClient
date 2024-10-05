import {Button} from "@nextui-org/react";
import {FaCaretDown} from "react-icons/fa";
import {useDispatch} from "react-redux";
import {setControlPanelIsOpen} from "app/slices/appSlice.ts";

export default function HideControlPanelButton() {
    const dispatch = useDispatch();

    const handleClick = () => {
        dispatch(setControlPanelIsOpen(false));
    };

    return (
        <div className='absolute -top-5 left-1/2'>
            <Button isIconOnly onPress={handleClick}>
                <FaCaretDown />
            </Button>
        </div>
    );
}
