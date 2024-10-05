import {Spinner} from "@nextui-org/react";
import useSpinnerModalState from "app/hooks/useSpinnerModalState.ts";

export default function SpinnerModal() {
    const {isOpen} = useSpinnerModalState();

    if (!isOpen) {
        return null;
    }

    return (
        <div
            className='absolute left-0 top-0 w-full h-full bg-black bg-opacity-50 z-1000 flex flex-row justify-center items-center'>
            <Spinner size='lg'/>
        </div>
    );
}
